"""
Attendance Service — Core Attendance Business Logic
Handles check-in, check-out, working minutes, late calculations, and audit logging.
"""
from datetime import datetime, date, time, timedelta
from app.extensions import db
from app.models.attendance import Attendance, AttendanceLog
from app.models.employee import AttendanceRule, Shift, EmployeeShift
from app.models.user import User

class AttendanceService:
    """Manages attendance check-in, check-out, shifts, and logs."""

    @staticmethod
    def record_attendance(organization_id: int, user_id: int, method: str = 'FACE',
                          confidence_score: float = None, ip_address: str = None,
                          device_id: str = None, lat: float = None, lng: float = None):
        """
        Records check-in or check-out for user_id on today's date.
        - First successful scan of the day = Check-in with exact server/database timestamp.
        - Minimum 4 hours (240 minutes) required between Check-in and Check-out.
        - Any scan before 4 hours does NOT create check-out.
        - After 4+ hours, the next scan = Check-out.
        - Handles duplicate scans and race conditions safely.
        """
        user = db.session.get(User, user_id)
        if not user:
            return 'ERROR', None, "User not found"

        today = date.today()
        now_dt = datetime.now()

        # Database locking to prevent race conditions during duplicate concurrent API requests
        try:
            attendance = Attendance.query.filter_by(
                organization_id=organization_id,
                user_id=user_id,
                attendance_date=today
            ).with_for_update().first()
        except Exception:
            attendance = Attendance.query.filter_by(
                organization_id=organization_id,
                user_id=user_id,
                attendance_date=today
            ).first()

        # Load organization attendance rule & default shift
        try:
            rule = AttendanceRule.query.filter_by(organization_id=organization_id).first()
        except Exception:
            db.session.rollback()
            rule = None
        late_grace = rule.late_grace_minutes if rule else 15

        MIN_CHECKOUT_MINUTES = 240  # 4 hours

        if not attendance or not attendance.check_in:
            # First check-in of the day
            shift_start = time(9, 0)  # Default 09:00 AM
            is_late = False
            late_mins = 0

            # Calculate late status
            shift_dt = datetime.combine(today, shift_start) + timedelta(minutes=late_grace)
            if now_dt > shift_dt:
                is_late = True
                late_mins = int((now_dt - datetime.combine(today, shift_start)).total_seconds() / 60)

            if not attendance:
                attendance = Attendance(
                    organization_id=organization_id,
                    user_id=user_id,
                    attendance_date=today,
                    check_in=now_dt,
                    check_in_method=method,
                    attendance_status='PRESENT',
                    confidence_score=confidence_score,
                    is_late=is_late,
                    late_minutes=late_mins,
                    check_in_latitude=lat,
                    check_in_longitude=lng,
                    device_id=device_id
                )
                db.session.add(attendance)
            else:
                attendance.check_in = now_dt
                attendance.check_in_method = method
                attendance.attendance_status = 'PRESENT'
                attendance.is_late = is_late
                attendance.late_minutes = late_mins

            db.session.flush()

            # Audit log
            try:
                log = AttendanceLog(
                    attendance_id=attendance.id,
                    organization_id=organization_id,
                    action='CHECK_IN',
                    changed_by=user_id,
                    action_time=now_dt,
                    ip_address=ip_address
                )
                db.session.add(log)
            except Exception:
                pass
            db.session.commit()

            return 'CHECK_IN', attendance.to_dict(), f"Check-in successful for {user.full_name} at {now_dt.strftime('%H:%M:%S')}"

        else:
            # Attendance record exists and check_in is already set
            in_dt = attendance.check_in if isinstance(attendance.check_in, datetime) else datetime.combine(today, attendance.check_in)

            # Check if checkout is already recorded
            if attendance.check_out is not None:
                out_dt = attendance.check_out if isinstance(attendance.check_out, datetime) else datetime.combine(today, attendance.check_out)
                in_str = in_dt.strftime('%H:%M:%S') if hasattr(in_dt, 'strftime') else str(in_dt)
                out_str = out_dt.strftime('%H:%M:%S') if hasattr(out_dt, 'strftime') else str(out_dt)
                return 'EXISTS', attendance.to_dict(), f"Attendance already completed for {user.full_name} today (Check-in: {in_str}, Check-out: {out_str})"

            # Calculate difference from check_in
            diff_seconds = (now_dt - in_dt).total_seconds()
            diff_mins = int(diff_seconds / 60)

            # Minimum 4 hours (240 minutes) requirement before Check-out
            if diff_mins < MIN_CHECKOUT_MINUTES:
                rem_mins_total = MIN_CHECKOUT_MINUTES - diff_mins
                rem_hrs = rem_mins_total // 60
                rem_mins = rem_mins_total % 60
                check_in_str = in_dt.strftime('%H:%M:%S') if hasattr(in_dt, 'strftime') else str(in_dt)

                if rem_hrs > 0 and rem_mins > 0:
                    rem_str = f"{rem_hrs}h {rem_mins}m"
                elif rem_hrs > 0:
                    rem_str = f"{rem_hrs}h"
                else:
                    rem_str = f"{rem_mins}m"

                return 'EXISTS', attendance.to_dict(), f"Checked in at {check_in_str}. Check-out is allowed only after 4 hours (Time remaining: {rem_str})."

            # 4+ hours passed: Record Check-out
            attendance.check_out = now_dt
            attendance.check_out_method = method
            attendance.working_minutes = diff_mins

            if lat and lng:
                attendance.check_out_latitude = lat
                attendance.check_out_longitude = lng

            # Audit log
            try:
                log = AttendanceLog(
                    attendance_id=attendance.id,
                    organization_id=organization_id,
                    action='CHECK_OUT',
                    changed_by=user_id,
                    action_time=now_dt,
                    ip_address=ip_address
                )
                db.session.add(log)
            except Exception:
                pass
            db.session.commit()

            hrs_worked = diff_mins // 60
            mins_worked = diff_mins % 60
            return 'CHECK_OUT', attendance.to_dict(), f"Check-out successful for {user.full_name} at {now_dt.strftime('%H:%M:%S')} ({hrs_worked}h {mins_worked}m worked)"
