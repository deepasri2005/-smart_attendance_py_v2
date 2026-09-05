"""
Comprehensive test suite for Face Attendance Enhancements:
- First scan check-in
- Under 4-hour check-out prevention
- 4+ hour check-out recording
- Duplicate scan prevention
- Race condition safety
- Database record validation
"""
import unittest
from datetime import datetime, date, timedelta
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.role import Role
from app.models.organization import Organization
from app.models.attendance import Attendance, AttendanceLog
from app.services.attendance_service import AttendanceService

class TestFaceAttendanceFlow(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Seed Organization and Users
        self.org = Organization(name="Test Corp", slug="TC01")
        db.session.add(self.org)
        db.session.flush()

        self.user1 = User(
            email="emp1@test.com",
            first_name="Employee",
            last_name="One",
            organization_id=self.org.id,
            is_active=True
        )
        db.session.add(self.user1)
        db.session.flush()
        self.user1_id = self.user1.id

        self.user2 = User(
            email="emp2@test.com",
            first_name="Employee",
            last_name="Two",
            organization_id=self.org.id,
            is_active=True
        )
        db.session.add(self.user2)
        db.session.flush()
        self.user2_id = self.user2.id

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_first_scan_creates_checkin(self):
        """Test #2: First scan of the day creates a Check-in record."""
        action, att_dict, msg = AttendanceService.record_attendance(
            organization_id=self.org.id,
            user_id=self.user1_id,
            method='FACE'
        )

        self.assertEqual(action, 'CHECK_IN')
        self.assertIn("Check-in successful", msg)
        self.assertIsNotNone(att_dict['check_in'])
        self.assertIsNone(att_dict['check_out'])

        # Verify Database
        rec = Attendance.query.filter_by(user_id=self.user1_id, attendance_date=date.today()).first()
        self.assertIsNotNone(rec)
        self.assertEqual(rec.check_in_method, 'FACE')
        self.assertEqual(rec.attendance_status, 'PRESENT')

        # Verify Audit Log
        log = AttendanceLog.query.filter_by(attendance_id=rec.id).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.action, 'CHECK_IN')

    def test_scan_before_4_hours_prevents_checkout(self):
        """Test #3 & #4: Any scan before 4 hours must NOT create checkout."""
        # Record Check-in at now - 2 hours (120 minutes ago)
        two_hours_ago = datetime.now() - timedelta(hours=2)
        att = Attendance(
            organization_id=self.org.id,
            user_id=self.user1_id,
            attendance_date=date.today(),
            check_in=two_hours_ago,
            check_in_method='FACE',
            attendance_status='PRESENT'
        )
        db.session.add(att)
        db.session.commit()

        # Scan again now (only 2 hours after check-in)
        action, att_dict, msg = AttendanceService.record_attendance(
            organization_id=self.org.id,
            user_id=self.user1_id,
            method='FACE'
        )

        self.assertEqual(action, 'EXISTS')
        self.assertIn("Check-out is allowed only after 4 hours", msg)
        self.assertIn("Time remaining", msg)
        self.assertIsNone(att_dict['check_out'])

        # DB Validation: Ensure check_out remains None
        rec = Attendance.query.filter_by(user_id=self.user1_id, attendance_date=date.today()).first()
        self.assertIsNone(rec.check_out)

    def test_scan_after_4_plus_hours_creates_checkout(self):
        """Test #5: Scan after 4+ hours creates a successful Check-out."""
        # Record Check-in at now - 4.5 hours (270 minutes ago)
        four_half_hours_ago = datetime.now() - timedelta(hours=4, minutes=30)
        att = Attendance(
            organization_id=self.org.id,
            user_id=self.user1_id,
            attendance_date=date.today(),
            check_in=four_half_hours_ago,
            check_in_method='FACE',
            attendance_status='PRESENT'
        )
        db.session.add(att)
        db.session.commit()

        # Scan again now (4.5 hours after check-in)
        action, att_dict, msg = AttendanceService.record_attendance(
            organization_id=self.org.id,
            user_id=self.user1_id,
            method='FACE'
        )

        self.assertEqual(action, 'CHECK_OUT')
        self.assertIn("Check-out successful", msg)
        self.assertIsNotNone(att_dict['check_out'])

        # DB Validation
        rec = Attendance.query.filter_by(user_id=self.user1_id, attendance_date=date.today()).first()
        self.assertIsNotNone(rec.check_out)
        self.assertGreaterEqual(rec.working_minutes, 270)

        # Audit Log check for checkout
        logs = AttendanceLog.query.filter_by(attendance_id=rec.id).all()
        actions = [l.action for l in logs]
        self.assertIn('CHECK_OUT', actions)

    def test_scan_after_checkout_prevents_duplicate_checkout(self):
        """Test #6: Duplicate scan after Check-out already completed."""
        four_hours_ago = datetime.now() - timedelta(hours=5)
        one_hour_ago = datetime.now() - timedelta(hours=1)
        att = Attendance(
            organization_id=self.org.id,
            user_id=self.user1_id,
            attendance_date=date.today(),
            check_in=four_hours_ago,
            check_out=one_hour_ago,
            check_in_method='FACE',
            check_out_method='FACE',
            working_minutes=240,
            attendance_status='PRESENT'
        )
        db.session.add(att)
        db.session.commit()

        # Scan again
        action, att_dict, msg = AttendanceService.record_attendance(
            organization_id=self.org.id,
            user_id=self.user1_id,
            method='FACE'
        )

        self.assertEqual(action, 'EXISTS')
        self.assertIn("Attendance already completed", msg)

    def test_multiple_users_isolation(self):
        """Test #9: Multiple users scanning independently on the same day."""
        # User 1 checks in
        act1, _, _ = AttendanceService.record_attendance(self.org.id, self.user1_id, 'FACE')
        self.assertEqual(act1, 'CHECK_IN')

        # User 2 checks in
        act2, _, _ = AttendanceService.record_attendance(self.org.id, self.user2_id, 'FACE')
        self.assertEqual(act2, 'CHECK_IN')

        # Both records exist independently
        count = Attendance.query.filter_by(attendance_date=date.today()).count()
        self.assertEqual(count, 2)


if __name__ == '__main__':
    unittest.main()
