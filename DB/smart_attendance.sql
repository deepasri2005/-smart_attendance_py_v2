-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 25, 2026 at 08:01 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smart_attendance`
--

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `attendance_date` date NOT NULL,
  `check_in` datetime DEFAULT NULL,
  `check_out` datetime DEFAULT NULL,
  `working_minutes` int(11) DEFAULT 0,
  `attendance_status` varchar(50) NOT NULL DEFAULT 'ABSENT',
  `check_in_method` varchar(50) DEFAULT NULL,
  `check_out_method` varchar(50) DEFAULT NULL,
  `check_in_latitude` decimal(10,8) DEFAULT NULL,
  `check_in_longitude` decimal(11,8) DEFAULT NULL,
  `check_out_latitude` decimal(10,8) DEFAULT NULL,
  `check_out_longitude` decimal(11,8) DEFAULT NULL,
  `check_in_location_accuracy` decimal(10,2) DEFAULT NULL,
  `check_out_location_accuracy` decimal(10,2) DEFAULT NULL,
  `check_in_distance_meters` decimal(10,2) DEFAULT NULL,
  `check_out_distance_meters` decimal(10,2) DEFAULT NULL,
  `check_in_image` varchar(500) DEFAULT NULL,
  `check_out_image` varchar(500) DEFAULT NULL,
  `confidence_score` decimal(6,4) DEFAULT NULL,
  `device_id` varchar(255) DEFAULT NULL,
  `is_late` tinyint(1) DEFAULT 0,
  `late_minutes` int(11) DEFAULT 0,
  `is_early_departure` tinyint(1) DEFAULT 0,
  `early_departure_minutes` int(11) DEFAULT 0,
  `overtime_minutes` int(11) DEFAULT 0,
  `approval_status` varchar(50) DEFAULT 'AUTO_APPROVED',
  `approved_by` bigint(20) UNSIGNED DEFAULT NULL,
  `approved_at` datetime DEFAULT NULL,
  `remarks` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `attendance_anomalies`
--

CREATE TABLE `attendance_anomalies` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `attendance_id` bigint(20) UNSIGNED DEFAULT NULL,
  `anomaly_type` varchar(150) NOT NULL,
  `severity` varchar(50) DEFAULT 'LOW',
  `description` text DEFAULT NULL,
  `detected_at` datetime DEFAULT current_timestamp(),
  `status` varchar(50) DEFAULT 'OPEN',
  `resolved_by` bigint(20) UNSIGNED DEFAULT NULL,
  `resolved_at` datetime DEFAULT NULL,
  `resolution_remarks` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `attendance_logs`
--

CREATE TABLE `attendance_logs` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `attendance_id` bigint(20) UNSIGNED DEFAULT NULL,
  `organization_id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `action_type` varchar(100) NOT NULL,
  `attendance_method` varchar(50) DEFAULT NULL,
  `action_time` datetime NOT NULL,
  `latitude` decimal(10,8) DEFAULT NULL,
  `longitude` decimal(11,8) DEFAULT NULL,
  `ip_address` varchar(50) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `image_path` varchar(500) DEFAULT NULL,
  `confidence_score` decimal(6,4) DEFAULT NULL,
  `remarks` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `attendance_regularization`
--

CREATE TABLE `attendance_regularization` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `attendance_id` bigint(20) UNSIGNED DEFAULT NULL,
  `request_type` varchar(100) NOT NULL,
  `requested_check_in` datetime DEFAULT NULL,
  `requested_check_out` datetime DEFAULT NULL,
  `reason` text NOT NULL,
  `attachment` varchar(500) DEFAULT NULL,
  `status` varchar(50) NOT NULL DEFAULT 'PENDING',
  `approved_by` bigint(20) UNSIGNED DEFAULT NULL,
  `approved_at` datetime DEFAULT NULL,
  `approver_remarks` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `audit_logs`
--

CREATE TABLE `audit_logs` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED DEFAULT NULL,
  `user_id` bigint(20) UNSIGNED DEFAULT NULL,
  `action` varchar(150) NOT NULL,
  `module` varchar(150) DEFAULT NULL,
  `record_type` varchar(150) DEFAULT NULL,
  `record_id` bigint(20) UNSIGNED DEFAULT NULL,
  `old_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`old_data`)),
  `new_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`new_data`)),
  `ip_address` varchar(50) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `audit_logs`
--

INSERT INTO `audit_logs` (`id`, `organization_id`, `user_id`, `action`, `module`, `record_type`, `record_id`, `old_data`, `new_data`, `ip_address`, `user_agent`, `created_at`) VALUES
(2, 1, 1, 'LOGIN', 'auth', NULL, NULL, NULL, '{\"description\": \"User admin logged in successfully\"}', NULL, NULL, '2026-08-25 00:03:10'),
(3, 1, 1, 'LOGIN', 'auth', NULL, NULL, NULL, '{\"description\": \"User admin logged in successfully\"}', NULL, NULL, '2026-08-25 00:10:24'),
(4, 1, 1, 'LOGIN', 'auth', NULL, NULL, NULL, '{\"description\": \"User admin logged in successfully\"}', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0', '2026-08-25 00:15:30'),
(5, 1, 1, 'LOGIN', 'auth', NULL, NULL, NULL, '{\"description\": \"User admin logged in successfully\"}', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0', '2026-08-25 00:15:51');

-- --------------------------------------------------------

--
-- Table structure for table `cctv_cameras`
--

CREATE TABLE `cctv_cameras` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED NOT NULL,
  `location_id` bigint(20) UNSIGNED DEFAULT NULL,
  `camera_name` varchar(150) NOT NULL,
  `camera_code` varchar(100) NOT NULL,
  `rtsp_url` text NOT NULL,
  `camera_username` varchar(150) DEFAULT NULL,
  `camera_password_encrypted` text DEFAULT NULL,
  `processing_interval_seconds` int(11) DEFAULT 5,
  `cooldown_minutes` int(11) DEFAULT 30,
  `is_active` tinyint(1) DEFAULT 1,
  `camera_status` varchar(30) DEFAULT 'OFFLINE',
  `last_seen_at` datetime DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cctv_cameras`
--

INSERT INTO `cctv_cameras` (`id`, `organization_id`, `location_id`, `camera_name`, `camera_code`, `rtsp_url`, `camera_username`, `camera_password_encrypted`, `processing_interval_seconds`, `cooldown_minutes`, `is_active`, `camera_status`, `last_seen_at`, `created_at`, `updated_at`) VALUES
(1, 1, NULL, 'Main Gate Entrance Cam', 'GATE-01', 'rtsp://admin:123456@192.168.1.100:554/live', NULL, NULL, 5, 30, 1, 'ONLINE', NULL, '2026-08-25 00:10:15', '2026-08-25 00:10:15');

-- --------------------------------------------------------

--
-- Table structure for table `cctv_detection_logs`
--

CREATE TABLE `cctv_detection_logs` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED NOT NULL,
  `camera_id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED DEFAULT NULL,
  `detection_time` datetime NOT NULL,
  `confidence_score` decimal(6,4) DEFAULT NULL,
  `image_path` varchar(500) DEFAULT NULL,
  `detection_status` varchar(50) NOT NULL DEFAULT 'UNKNOWN',
  `attendance_marked` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `departments`
--

CREATE TABLE `departments` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED NOT NULL,
  `department_name` varchar(150) NOT NULL,
  `department_code` varchar(50) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `designations`
--

CREATE TABLE `designations` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED NOT NULL,
  `designation_name` varchar(150) NOT NULL,
  `designation_code` varchar(50) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `device_registrations`
--

CREATE TABLE `device_registrations` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED DEFAULT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `device_id` varchar(255) NOT NULL,
  `device_name` varchar(255) DEFAULT NULL,
  `browser` varchar(150) DEFAULT NULL,
  `operating_system` varchar(150) DEFAULT NULL,
  `ip_address` varchar(50) DEFAULT NULL,
  `is_trusted` tinyint(1) DEFAULT 0,
  `is_active` tinyint(1) DEFAULT 1,
  `last_login` datetime DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `employee_shifts`
--

CREATE TABLE `employee_shifts` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `shift_id` bigint(20) UNSIGNED NOT NULL,
  `effective_from` date NOT NULL,
  `effective_to` date DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `face_encodings`
--

CREATE TABLE `face_encodings` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `face_profile_id` bigint(20) UNSIGNED NOT NULL,
  `image_path` varchar(500) DEFAULT NULL,
  `face_encoding` longblob NOT NULL,
  `encoding_version` varchar(50) DEFAULT NULL,
  `quality_score` decimal(5,2) DEFAULT NULL,
  `is_primary` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `face_encodings`
--

INSERT INTO `face_encodings` (`id`, `face_profile_id`, `image_path`, `face_encoding`, `encoding_version`, `quality_score`, `is_primary`, `created_at`) VALUES
(1, 1, NULL, 0x14f47e000000d03f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000247dfd6083f2cf3fc928caa06d7a593f0000000000000000000000000000000000000000000000000000000000000000000000000000000012a4e7a09d318d3fa879fd0013f2cf3f0275a8a0103b553f0000000000000000000000000000000000000000000000000000000000000000000000000000000002d7eb4017b98d3f14f47e000000d03f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000014f47e000000d03f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004401e040403bbc3f4e269120144b923f000000000000000000000000000000000000000000000000000000000000000000000000000000002b25e34091a0cc3ffb9ad660fc0bbb3fd7e3e060ce578c3f0000000000000000000000000000000000000000000000000000000000000000000000000000000082b0e5e0a7f2cc3f14f47e000000d03f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000014f47e000000d03f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000268cbae0ba82b73f9be0bf80b12e883f000000000000000000000000000000000000000000000000000000000000000000000000000000006ad9ebe064b9cd3fe50fb540c0d1b63f25c098605040833f00000000000000000000000000000000000000000000000000000000000000000000000000000000d806ed2062dfcd3f14f47e000000d03f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000014f47e000000d03f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000db74fd2078f1cf3fdf8dca002b87593f000000000000000000000000000000000000000000000000000000000000000000000000000000007888f00083508e3f1a6ffd60bef0cf3f6d7287c00812613f00000000000000000000000000000000000000000000000000000000000000000000000000000000657ff5e0aff08e3f14f47e000000d03f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000, NULL, NULL, 1, '2026-08-25 00:10:24');

-- --------------------------------------------------------

--
-- Table structure for table `face_profiles`
--

CREATE TABLE `face_profiles` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `face_status` varchar(30) DEFAULT 'PENDING',
  `registered_by` bigint(20) UNSIGNED DEFAULT NULL,
  `registered_at` datetime DEFAULT NULL,
  `last_verified_at` datetime DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `face_profiles`
--

INSERT INTO `face_profiles` (`id`, `organization_id`, `user_id`, `face_status`, `registered_by`, `registered_at`, `last_verified_at`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 1, 1, 'PENDING', NULL, NULL, NULL, 1, '2026-08-25 00:10:24', '2026-08-25 00:10:24');

-- --------------------------------------------------------

--
-- Table structure for table `holidays`
--

CREATE TABLE `holidays` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED NOT NULL,
  `holiday_name` varchar(255) NOT NULL,
  `holiday_date` date NOT NULL,
  `holiday_type` varchar(50) DEFAULT 'GENERAL',
  `description` text DEFAULT NULL,
  `is_optional` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `leave_applications`
--

CREATE TABLE `leave_applications` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `leave_type_id` bigint(20) UNSIGNED NOT NULL,
  `from_date` date NOT NULL,
  `to_date` date NOT NULL,
  `total_days` decimal(6,2) NOT NULL,
  `is_half_day` tinyint(1) DEFAULT 0,
  `half_day_type` varchar(50) DEFAULT NULL,
  `reason` text NOT NULL,
  `attachment` varchar(500) DEFAULT NULL,
  `status` varchar(50) NOT NULL DEFAULT 'PENDING',
  `approved_by` bigint(20) UNSIGNED DEFAULT NULL,
  `approved_at` datetime DEFAULT NULL,
  `approver_remarks` text DEFAULT NULL,
  `cancelled_at` datetime DEFAULT NULL,
  `cancellation_reason` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `leave_balances`
--

CREATE TABLE `leave_balances` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `leave_type_id` bigint(20) UNSIGNED NOT NULL,
  `leave_year` year(4) NOT NULL,
  `allocated_days` decimal(6,2) DEFAULT 0.00,
  `used_days` decimal(6,2) DEFAULT 0.00,
  `remaining_days` decimal(6,2) DEFAULT 0.00,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `leave_types`
--

CREATE TABLE `leave_types` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED NOT NULL,
  `leave_name` varchar(150) NOT NULL,
  `leave_code` varchar(50) NOT NULL,
  `total_days_per_year` decimal(6,2) DEFAULT 0.00,
  `is_paid` tinyint(1) DEFAULT 1,
  `allow_half_day` tinyint(1) DEFAULT 1,
  `requires_document` tinyint(1) DEFAULT 0,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `login_details`
--

CREATE TABLE `login_details` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED DEFAULT NULL,
  `role_id` bigint(20) UNSIGNED NOT NULL,
  `username` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(150) DEFAULT NULL,
  `mobile_number` varchar(20) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `failed_login_attempts` int(11) NOT NULL DEFAULT 0,
  `locked_until` datetime DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `password_changed_at` datetime DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `login_details`
--

INSERT INTO `login_details` (`id`, `user_id`, `organization_id`, `role_id`, `username`, `password_hash`, `email`, `mobile_number`, `is_active`, `failed_login_attempts`, `locked_until`, `last_login`, `password_changed_at`, `created_at`, `updated_at`) VALUES
(1, 1, 1, 1, 'admin', '$2b$12$sDcQJZNiKYlPj134ahQdfeUyxs82H8e5wgJjj93/ppIwm3LcG8W9S', 'admin@smartattend.com', NULL, 1, 0, NULL, '2026-08-25 05:45:51', NULL, '2026-08-25 05:28:59', '2026-08-25 00:15:51');

-- --------------------------------------------------------

--
-- Table structure for table `login_history`
--

CREATE TABLE `login_history` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED DEFAULT NULL,
  `organization_id` bigint(20) UNSIGNED DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  `login_status` varchar(50) NOT NULL,
  `ip_address` varchar(50) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `failure_reason` varchar(255) DEFAULT NULL,
  `login_at` datetime DEFAULT current_timestamp(),
  `logout_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `login_history`
--

INSERT INTO `login_history` (`id`, `user_id`, `organization_id`, `username`, `login_status`, `ip_address`, `user_agent`, `failure_reason`, `login_at`, `logout_at`) VALUES
(1, 1, NULL, 'admin', 'SUCCESS', NULL, NULL, NULL, '2026-08-25 05:33:10', NULL),
(2, 1, NULL, 'admin', 'SUCCESS', NULL, NULL, NULL, '2026-08-25 05:40:24', NULL),
(3, 1, NULL, 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0', NULL, '2026-08-25 05:45:30', NULL),
(4, 1, NULL, 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0', NULL, '2026-08-25 05:45:51', NULL),
(5, NULL, NULL, 'orgadmin_test', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0', NULL, '2026-08-25 05:46:17', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `modules`
--

CREATE TABLE `modules` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `module_name` varchar(150) NOT NULL,
  `module_slug` varchar(150) NOT NULL,
  `module_icon` varchar(100) DEFAULT NULL,
  `route_name` varchar(255) DEFAULT NULL,
  `display_order` int(11) DEFAULT 0,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `modules`
--

INSERT INTO `modules` (`id`, `module_name`, `module_slug`, `module_icon`, `route_name`, `display_order`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 'Dashboard', 'dashboard', 'dashboard', NULL, 1, 1, '2026-08-25 05:21:15', '2026-08-25 05:21:15'),
(2, 'Organization Management', 'organization_management', 'building', NULL, 2, 1, '2026-08-25 05:21:15', '2026-08-25 05:21:15'),
(3, 'Employee Management', 'employee_management', 'users', NULL, 3, 1, '2026-08-25 05:21:15', '2026-08-25 05:21:15'),
(4, 'Attendance', 'attendance', 'calendar-check', NULL, 4, 1, '2026-08-25 05:21:15', '2026-08-25 05:21:15'),
(5, 'Leave Management', 'leave', 'calendar-minus', NULL, 5, 1, '2026-08-25 05:21:15', '2026-08-25 05:21:15'),
(6, 'Tour Management', 'tour', 'map', NULL, 6, 1, '2026-08-25 05:21:15', '2026-08-25 05:21:15'),
(7, 'Work From Home', 'work_from_home', 'house', NULL, 7, 1, '2026-08-25 05:21:15', '2026-08-25 05:21:15'),
(8, 'Notifications', 'notifications', 'bell', NULL, 8, 1, '2026-08-25 05:21:15', '2026-08-25 05:21:15'),
(9, 'Reports', 'reports', 'bar-chart', NULL, 9, 1, '2026-08-25 05:21:15', '2026-08-25 05:21:15'),
(10, 'Settings', 'settings', 'gear', NULL, 10, 1, '2026-08-25 05:21:15', '2026-08-25 05:21:15'),
(11, 'Audit Logs', 'audit_logs', 'clock-history', NULL, 11, 1, '2026-08-25 05:21:15', '2026-08-25 05:21:15');

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED DEFAULT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `title` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `notification_type` varchar(50) DEFAULT 'IN_APP',
  `reference_type` varchar(100) DEFAULT NULL,
  `reference_id` bigint(20) UNSIGNED DEFAULT NULL,
  `is_read` tinyint(1) DEFAULT 0,
  `read_at` datetime DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `organizations`
--

CREATE TABLE `organizations` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_code` varchar(50) NOT NULL,
  `organization_name` varchar(255) NOT NULL,
  `email` varchar(150) DEFAULT NULL,
  `mobile_number` varchar(20) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `country` varchar(100) DEFAULT 'India',
  `pincode` varchar(20) DEFAULT NULL,
  `logo` varchar(500) DEFAULT NULL,
  `website` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `organizations`
--

INSERT INTO `organizations` (`id`, `organization_code`, `organization_name`, `email`, `mobile_number`, `address`, `city`, `state`, `country`, `pincode`, `logo`, `website`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 'HQ', 'SmartAttend HQ', 'admin@smartattend.com', NULL, NULL, NULL, NULL, 'India', NULL, NULL, NULL, 1, '2026-08-25 05:28:59', '2026-08-25 05:28:59');

-- --------------------------------------------------------

--
-- Table structure for table `organization_locations`
--

CREATE TABLE `organization_locations` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED NOT NULL,
  `location_name` varchar(150) NOT NULL,
  `address` text DEFAULT NULL,
  `latitude` decimal(10,8) NOT NULL,
  `longitude` decimal(11,8) NOT NULL,
  `allowed_radius_meters` int(11) NOT NULL DEFAULT 100,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `permissions`
--

CREATE TABLE `permissions` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `permission_name` varchar(150) NOT NULL,
  `permission_slug` varchar(150) NOT NULL,
  `description` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `permissions`
--

INSERT INTO `permissions` (`id`, `permission_name`, `permission_slug`, `description`, `created_at`) VALUES
(1, 'View', 'view', 'View records', '2026-08-25 05:21:15'),
(2, 'Create', 'create', 'Create records', '2026-08-25 05:21:15'),
(3, 'Edit', 'edit', 'Edit records', '2026-08-25 05:21:15'),
(4, 'Delete', 'delete', 'Delete records', '2026-08-25 05:21:15'),
(5, 'Approve', 'approve', 'Approve requests', '2026-08-25 05:21:15'),
(6, 'Reject', 'reject', 'Reject requests', '2026-08-25 05:21:15'),
(7, 'Export', 'export', 'Export reports', '2026-08-25 05:21:15'),
(8, 'Manage', 'manage', 'Full management access', '2026-08-25 05:21:15');

-- --------------------------------------------------------

--
-- Table structure for table `refresh_tokens`
--

CREATE TABLE `refresh_tokens` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `jti` varchar(255) NOT NULL,
  `token_hash` varchar(255) DEFAULT NULL,
  `expires_at` datetime NOT NULL,
  `is_revoked` tinyint(1) DEFAULT 0,
  `revoked_at` datetime DEFAULT NULL,
  `device_id` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `role_name` varchar(100) NOT NULL,
  `role_slug` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `is_system_role` tinyint(1) DEFAULT 0,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`id`, `role_name`, `role_slug`, `description`, `is_system_role`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 'Super Admin', 'super_admin', 'Complete system access', 1, 1, '2026-08-25 05:21:15', '2026-08-25 05:21:15'),
(2, 'Organization Admin', 'org_admin', 'Organization level administrator', 1, 1, '2026-08-25 05:21:15', '2026-08-25 05:21:15'),
(3, 'Employee Admin', 'emp_admin', 'Attendance and employee administration', 1, 1, '2026-08-25 05:21:15', '2026-08-25 05:21:15'),
(4, 'Employee', 'emp', 'Regular employee', 1, 1, '2026-08-25 05:21:15', '2026-08-25 05:21:15');

-- --------------------------------------------------------

--
-- Table structure for table `role_permissions`
--

CREATE TABLE `role_permissions` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `role_id` bigint(20) UNSIGNED NOT NULL,
  `module_id` bigint(20) UNSIGNED DEFAULT NULL,
  `sub_module_id` bigint(20) UNSIGNED DEFAULT NULL,
  `permission_id` bigint(20) UNSIGNED NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `shifts`
--

CREATE TABLE `shifts` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED NOT NULL,
  `shift_name` varchar(150) NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `grace_minutes` int(11) DEFAULT 0,
  `minimum_working_minutes` int(11) DEFAULT 480,
  `half_day_minutes` int(11) DEFAULT 240,
  `allow_late_checkin` tinyint(1) DEFAULT 1,
  `allow_early_checkout` tinyint(1) DEFAULT 1,
  `is_night_shift` tinyint(1) DEFAULT 0,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sub_modules`
--

CREATE TABLE `sub_modules` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `module_id` bigint(20) UNSIGNED NOT NULL,
  `sub_module_name` varchar(150) NOT NULL,
  `sub_module_slug` varchar(150) NOT NULL,
  `route_name` varchar(255) DEFAULT NULL,
  `display_order` int(11) DEFAULT 0,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sub_modules`
--

INSERT INTO `sub_modules` (`id`, `module_id`, `sub_module_name`, `sub_module_slug`, `route_name`, `display_order`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 4, 'Face Attendance', 'face_attendance', NULL, 1, 1, '2026-08-25 05:21:15', '2026-08-25 05:21:15'),
(2, 4, 'CCTV Attendance', 'cctv_attendance', NULL, 2, 1, '2026-08-25 05:21:16', '2026-08-25 05:21:16'),
(3, 4, 'Geo Attendance', 'geo_attendance', NULL, 3, 1, '2026-08-25 05:21:16', '2026-08-25 05:21:16'),
(4, 4, 'Manual Attendance', 'manual_attendance', NULL, 4, 1, '2026-08-25 05:21:16', '2026-08-25 05:21:16'),
(5, 4, 'Attendance Regularization', 'attendance_regularization', NULL, 5, 1, '2026-08-25 05:21:16', '2026-08-25 05:21:16'),
(6, 4, 'Attendance Approval', 'attendance_approval', NULL, 6, 1, '2026-08-25 05:21:16', '2026-08-25 05:21:16');

-- --------------------------------------------------------

--
-- Table structure for table `system_settings`
--

CREATE TABLE `system_settings` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED DEFAULT NULL,
  `setting_key` varchar(150) NOT NULL,
  `setting_value` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tour_applications`
--

CREATE TABLE `tour_applications` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `from_date` date NOT NULL,
  `to_date` date NOT NULL,
  `tour_location` varchar(255) NOT NULL,
  `purpose` text NOT NULL,
  `estimated_expense` decimal(12,2) DEFAULT 0.00,
  `travel_details` text DEFAULT NULL,
  `attachment` varchar(500) DEFAULT NULL,
  `status` varchar(50) DEFAULT 'PENDING',
  `approved_by` bigint(20) UNSIGNED DEFAULT NULL,
  `approved_at` datetime DEFAULT NULL,
  `approver_remarks` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED DEFAULT NULL,
  `employee_code` varchar(100) DEFAULT NULL,
  `first_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `mobile_number` varchar(20) DEFAULT NULL,
  `department_id` bigint(20) UNSIGNED DEFAULT NULL,
  `designation_id` bigint(20) UNSIGNED DEFAULT NULL,
  `reporting_manager_id` bigint(20) UNSIGNED DEFAULT NULL,
  `profile_image` varchar(500) DEFAULT NULL,
  `date_of_joining` date DEFAULT NULL,
  `employment_type` varchar(50) DEFAULT 'FULL_TIME',
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `created_by` bigint(20) UNSIGNED DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `organization_id`, `employee_code`, `first_name`, `middle_name`, `last_name`, `email`, `mobile_number`, `department_id`, `designation_id`, `reporting_manager_id`, `profile_image`, `date_of_joining`, `employment_type`, `is_active`, `created_by`, `created_at`, `updated_at`) VALUES
(1, 1, 'EMP001', 'Super', NULL, 'Admin', 'admin@smartattend.com', NULL, NULL, NULL, NULL, NULL, NULL, 'FULL_TIME', 1, NULL, '2026-08-25 05:28:59', '2026-08-25 05:28:59');

-- --------------------------------------------------------

--
-- Table structure for table `user_permissions`
--

CREATE TABLE `user_permissions` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `module_id` bigint(20) UNSIGNED DEFAULT NULL,
  `sub_module_id` bigint(20) UNSIGNED DEFAULT NULL,
  `permission_id` bigint(20) UNSIGNED NOT NULL,
  `granted_by` bigint(20) UNSIGNED DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Stand-in structure for view `vw_daily_attendance`
-- (See below for the actual view)
--
CREATE TABLE `vw_daily_attendance` (
`id` bigint(20) unsigned
,`organization_id` bigint(20) unsigned
,`user_id` bigint(20) unsigned
,`employee_name` varchar(302)
,`employee_code` varchar(100)
,`attendance_date` date
,`check_in` datetime
,`check_out` datetime
,`working_minutes` int(11)
,`attendance_status` varchar(50)
,`check_in_method` varchar(50)
,`check_out_method` varchar(50)
,`is_late` tinyint(1)
,`late_minutes` int(11)
,`overtime_minutes` int(11)
);

-- --------------------------------------------------------

--
-- Table structure for table `wfh_applications`
--

CREATE TABLE `wfh_applications` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `organization_id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `from_date` date NOT NULL,
  `to_date` date NOT NULL,
  `is_partial_day` tinyint(1) DEFAULT 0,
  `work_location` varchar(500) DEFAULT NULL,
  `reason` text NOT NULL,
  `status` varchar(50) DEFAULT 'PENDING',
  `approved_by` bigint(20) UNSIGNED DEFAULT NULL,
  `approved_at` datetime DEFAULT NULL,
  `approver_remarks` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure for view `vw_daily_attendance`
--
DROP TABLE IF EXISTS `vw_daily_attendance`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_daily_attendance`  AS SELECT `a`.`id` AS `id`, `a`.`organization_id` AS `organization_id`, `a`.`user_id` AS `user_id`, concat_ws(' ',`u`.`first_name`,`u`.`middle_name`,`u`.`last_name`) AS `employee_name`, `u`.`employee_code` AS `employee_code`, `a`.`attendance_date` AS `attendance_date`, `a`.`check_in` AS `check_in`, `a`.`check_out` AS `check_out`, `a`.`working_minutes` AS `working_minutes`, `a`.`attendance_status` AS `attendance_status`, `a`.`check_in_method` AS `check_in_method`, `a`.`check_out_method` AS `check_out_method`, `a`.`is_late` AS `is_late`, `a`.`late_minutes` AS `late_minutes`, `a`.`overtime_minutes` AS `overtime_minutes` FROM (`attendance` `a` join `users` `u` on(`u`.`id` = `a`.`user_id`))  ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_daily_attendance` (`organization_id`,`user_id`,`attendance_date`),
  ADD KEY `approved_by` (`approved_by`),
  ADD KEY `idx_attendance_org_date` (`organization_id`,`attendance_date`),
  ADD KEY `idx_attendance_user_date` (`user_id`,`attendance_date`),
  ADD KEY `idx_attendance_status` (`attendance_status`);

--
-- Indexes for table `attendance_anomalies`
--
ALTER TABLE `attendance_anomalies`
  ADD PRIMARY KEY (`id`),
  ADD KEY `organization_id` (`organization_id`),
  ADD KEY `attendance_id` (`attendance_id`),
  ADD KEY `resolved_by` (`resolved_by`),
  ADD KEY `idx_anomaly_user` (`user_id`),
  ADD KEY `idx_anomaly_status` (`status`);

--
-- Indexes for table `attendance_logs`
--
ALTER TABLE `attendance_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `attendance_id` (`attendance_id`),
  ADD KEY `organization_id` (`organization_id`),
  ADD KEY `idx_attendance_log_user_time` (`user_id`,`action_time`);

--
-- Indexes for table `attendance_regularization`
--
ALTER TABLE `attendance_regularization`
  ADD PRIMARY KEY (`id`),
  ADD KEY `organization_id` (`organization_id`),
  ADD KEY `attendance_id` (`attendance_id`),
  ADD KEY `approved_by` (`approved_by`),
  ADD KEY `idx_regularization_user` (`user_id`),
  ADD KEY `idx_regularization_status` (`status`);

--
-- Indexes for table `audit_logs`
--
ALTER TABLE `audit_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_audit_org` (`organization_id`),
  ADD KEY `idx_audit_user` (`user_id`),
  ADD KEY `idx_audit_record` (`record_type`,`record_id`),
  ADD KEY `idx_audit_created` (`created_at`);

--
-- Indexes for table `cctv_cameras`
--
ALTER TABLE `cctv_cameras`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_org_camera_code` (`organization_id`,`camera_code`),
  ADD KEY `location_id` (`location_id`);

--
-- Indexes for table `cctv_detection_logs`
--
ALTER TABLE `cctv_detection_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `organization_id` (`organization_id`),
  ADD KEY `camera_id` (`camera_id`),
  ADD KEY `idx_cctv_detection_time` (`detection_time`),
  ADD KEY `idx_cctv_user_time` (`user_id`,`detection_time`);

--
-- Indexes for table `departments`
--
ALTER TABLE `departments`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_org_department` (`organization_id`,`department_name`);

--
-- Indexes for table `designations`
--
ALTER TABLE `designations`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_org_designation` (`organization_id`,`designation_name`);

--
-- Indexes for table `device_registrations`
--
ALTER TABLE `device_registrations`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_user_device` (`user_id`,`device_id`),
  ADD KEY `organization_id` (`organization_id`);

--
-- Indexes for table `employee_shifts`
--
ALTER TABLE `employee_shifts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `organization_id` (`organization_id`),
  ADD KEY `shift_id` (`shift_id`),
  ADD KEY `idx_employee_shift_user` (`user_id`),
  ADD KEY `idx_employee_shift_dates` (`effective_from`,`effective_to`);

--
-- Indexes for table `face_encodings`
--
ALTER TABLE `face_encodings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_face_profile` (`face_profile_id`);

--
-- Indexes for table `face_profiles`
--
ALTER TABLE `face_profiles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_user_face_profile` (`user_id`),
  ADD KEY `organization_id` (`organization_id`),
  ADD KEY `registered_by` (`registered_by`);

--
-- Indexes for table `holidays`
--
ALTER TABLE `holidays`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_org_holiday` (`organization_id`,`holiday_date`);

--
-- Indexes for table `leave_applications`
--
ALTER TABLE `leave_applications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `organization_id` (`organization_id`),
  ADD KEY `leave_type_id` (`leave_type_id`),
  ADD KEY `approved_by` (`approved_by`),
  ADD KEY `idx_leave_user_dates` (`user_id`,`from_date`,`to_date`),
  ADD KEY `idx_leave_status` (`status`);

--
-- Indexes for table `leave_balances`
--
ALTER TABLE `leave_balances`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_user_leave_balance` (`user_id`,`leave_type_id`,`leave_year`),
  ADD KEY `organization_id` (`organization_id`),
  ADD KEY `leave_type_id` (`leave_type_id`);

--
-- Indexes for table `leave_types`
--
ALTER TABLE `leave_types`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_org_leave_type` (`organization_id`,`leave_code`);

--
-- Indexes for table `login_details`
--
ALTER TABLE `login_details`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `uk_login_user` (`user_id`),
  ADD KEY `idx_login_username` (`username`),
  ADD KEY `idx_login_org` (`organization_id`),
  ADD KEY `idx_login_role` (`role_id`);

--
-- Indexes for table `login_history`
--
ALTER TABLE `login_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `organization_id` (`organization_id`),
  ADD KEY `idx_login_history_user` (`user_id`,`login_at`);

--
-- Indexes for table `modules`
--
ALTER TABLE `modules`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `module_slug` (`module_slug`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `organization_id` (`organization_id`),
  ADD KEY `idx_notification_user_read` (`user_id`,`is_read`);

--
-- Indexes for table `organizations`
--
ALTER TABLE `organizations`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `organization_code` (`organization_code`),
  ADD KEY `idx_organization_code` (`organization_code`),
  ADD KEY `idx_organization_active` (`is_active`);

--
-- Indexes for table `organization_locations`
--
ALTER TABLE `organization_locations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_location_org` (`organization_id`);

--
-- Indexes for table `permissions`
--
ALTER TABLE `permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `permission_slug` (`permission_slug`);

--
-- Indexes for table `refresh_tokens`
--
ALTER TABLE `refresh_tokens`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `jti` (`jti`),
  ADD KEY `idx_token_user` (`user_id`),
  ADD KEY `idx_token_expires` (`expires_at`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `role_name` (`role_name`),
  ADD UNIQUE KEY `role_slug` (`role_slug`);

--
-- Indexes for table `role_permissions`
--
ALTER TABLE `role_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_role_permission` (`role_id`,`module_id`,`sub_module_id`,`permission_id`),
  ADD KEY `module_id` (`module_id`),
  ADD KEY `sub_module_id` (`sub_module_id`),
  ADD KEY `permission_id` (`permission_id`);

--
-- Indexes for table `shifts`
--
ALTER TABLE `shifts`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_org_shift` (`organization_id`,`shift_name`);

--
-- Indexes for table `sub_modules`
--
ALTER TABLE `sub_modules`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_module_submodule` (`module_id`,`sub_module_slug`);

--
-- Indexes for table `system_settings`
--
ALTER TABLE `system_settings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_org_setting` (`organization_id`,`setting_key`);

--
-- Indexes for table `tour_applications`
--
ALTER TABLE `tour_applications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `organization_id` (`organization_id`),
  ADD KEY `approved_by` (`approved_by`),
  ADD KEY `idx_tour_user_dates` (`user_id`,`from_date`,`to_date`),
  ADD KEY `idx_tour_status` (`status`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_org_employee_code` (`organization_id`,`employee_code`),
  ADD KEY `designation_id` (`designation_id`),
  ADD KEY `reporting_manager_id` (`reporting_manager_id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `idx_user_org` (`organization_id`),
  ADD KEY `idx_user_department` (`department_id`),
  ADD KEY `idx_user_email` (`email`),
  ADD KEY `idx_user_mobile` (`mobile_number`);

--
-- Indexes for table `user_permissions`
--
ALTER TABLE `user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `module_id` (`module_id`),
  ADD KEY `sub_module_id` (`sub_module_id`),
  ADD KEY `permission_id` (`permission_id`),
  ADD KEY `granted_by` (`granted_by`);

--
-- Indexes for table `wfh_applications`
--
ALTER TABLE `wfh_applications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `organization_id` (`organization_id`),
  ADD KEY `approved_by` (`approved_by`),
  ADD KEY `idx_wfh_user_dates` (`user_id`,`from_date`,`to_date`),
  ADD KEY `idx_wfh_status` (`status`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `attendance_anomalies`
--
ALTER TABLE `attendance_anomalies`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `attendance_logs`
--
ALTER TABLE `attendance_logs`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `attendance_regularization`
--
ALTER TABLE `attendance_regularization`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `audit_logs`
--
ALTER TABLE `audit_logs`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `cctv_cameras`
--
ALTER TABLE `cctv_cameras`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `cctv_detection_logs`
--
ALTER TABLE `cctv_detection_logs`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `departments`
--
ALTER TABLE `departments`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `designations`
--
ALTER TABLE `designations`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `device_registrations`
--
ALTER TABLE `device_registrations`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `employee_shifts`
--
ALTER TABLE `employee_shifts`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `face_encodings`
--
ALTER TABLE `face_encodings`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `face_profiles`
--
ALTER TABLE `face_profiles`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `holidays`
--
ALTER TABLE `holidays`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `leave_applications`
--
ALTER TABLE `leave_applications`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `leave_balances`
--
ALTER TABLE `leave_balances`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `leave_types`
--
ALTER TABLE `leave_types`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `login_details`
--
ALTER TABLE `login_details`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `login_history`
--
ALTER TABLE `login_history`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `modules`
--
ALTER TABLE `modules`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `organizations`
--
ALTER TABLE `organizations`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `organization_locations`
--
ALTER TABLE `organization_locations`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `permissions`
--
ALTER TABLE `permissions`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `refresh_tokens`
--
ALTER TABLE `refresh_tokens`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `role_permissions`
--
ALTER TABLE `role_permissions`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `shifts`
--
ALTER TABLE `shifts`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sub_modules`
--
ALTER TABLE `sub_modules`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `system_settings`
--
ALTER TABLE `system_settings`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tour_applications`
--
ALTER TABLE `tour_applications`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `user_permissions`
--
ALTER TABLE `user_permissions`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `wfh_applications`
--
ALTER TABLE `wfh_applications`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `attendance`
--
ALTER TABLE `attendance`
  ADD CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `attendance_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `attendance_ibfk_3` FOREIGN KEY (`approved_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `attendance_anomalies`
--
ALTER TABLE `attendance_anomalies`
  ADD CONSTRAINT `attendance_anomalies_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `attendance_anomalies_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `attendance_anomalies_ibfk_3` FOREIGN KEY (`attendance_id`) REFERENCES `attendance` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `attendance_anomalies_ibfk_4` FOREIGN KEY (`resolved_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `attendance_logs`
--
ALTER TABLE `attendance_logs`
  ADD CONSTRAINT `attendance_logs_ibfk_1` FOREIGN KEY (`attendance_id`) REFERENCES `attendance` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `attendance_logs_ibfk_2` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `attendance_logs_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `attendance_regularization`
--
ALTER TABLE `attendance_regularization`
  ADD CONSTRAINT `attendance_regularization_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `attendance_regularization_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `attendance_regularization_ibfk_3` FOREIGN KEY (`attendance_id`) REFERENCES `attendance` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `attendance_regularization_ibfk_4` FOREIGN KEY (`approved_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `audit_logs`
--
ALTER TABLE `audit_logs`
  ADD CONSTRAINT `audit_logs_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `audit_logs_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `cctv_cameras`
--
ALTER TABLE `cctv_cameras`
  ADD CONSTRAINT `cctv_cameras_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `cctv_cameras_ibfk_2` FOREIGN KEY (`location_id`) REFERENCES `organization_locations` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `cctv_detection_logs`
--
ALTER TABLE `cctv_detection_logs`
  ADD CONSTRAINT `cctv_detection_logs_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `cctv_detection_logs_ibfk_2` FOREIGN KEY (`camera_id`) REFERENCES `cctv_cameras` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `cctv_detection_logs_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `departments`
--
ALTER TABLE `departments`
  ADD CONSTRAINT `departments_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `designations`
--
ALTER TABLE `designations`
  ADD CONSTRAINT `designations_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `device_registrations`
--
ALTER TABLE `device_registrations`
  ADD CONSTRAINT `device_registrations_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `device_registrations_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `employee_shifts`
--
ALTER TABLE `employee_shifts`
  ADD CONSTRAINT `employee_shifts_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `employee_shifts_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `employee_shifts_ibfk_3` FOREIGN KEY (`shift_id`) REFERENCES `shifts` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `face_encodings`
--
ALTER TABLE `face_encodings`
  ADD CONSTRAINT `face_encodings_ibfk_1` FOREIGN KEY (`face_profile_id`) REFERENCES `face_profiles` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `face_profiles`
--
ALTER TABLE `face_profiles`
  ADD CONSTRAINT `face_profiles_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `face_profiles_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `face_profiles_ibfk_3` FOREIGN KEY (`registered_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `holidays`
--
ALTER TABLE `holidays`
  ADD CONSTRAINT `holidays_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `leave_applications`
--
ALTER TABLE `leave_applications`
  ADD CONSTRAINT `leave_applications_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `leave_applications_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `leave_applications_ibfk_3` FOREIGN KEY (`leave_type_id`) REFERENCES `leave_types` (`id`),
  ADD CONSTRAINT `leave_applications_ibfk_4` FOREIGN KEY (`approved_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `leave_balances`
--
ALTER TABLE `leave_balances`
  ADD CONSTRAINT `leave_balances_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `leave_balances_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `leave_balances_ibfk_3` FOREIGN KEY (`leave_type_id`) REFERENCES `leave_types` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `leave_types`
--
ALTER TABLE `leave_types`
  ADD CONSTRAINT `leave_types_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `login_details`
--
ALTER TABLE `login_details`
  ADD CONSTRAINT `login_details_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `login_details_ibfk_2` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `login_details_ibfk_3` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);

--
-- Constraints for table `login_history`
--
ALTER TABLE `login_history`
  ADD CONSTRAINT `login_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `login_history_ibfk_2` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `notifications_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `organization_locations`
--
ALTER TABLE `organization_locations`
  ADD CONSTRAINT `organization_locations_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `refresh_tokens`
--
ALTER TABLE `refresh_tokens`
  ADD CONSTRAINT `refresh_tokens_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `role_permissions`
--
ALTER TABLE `role_permissions`
  ADD CONSTRAINT `role_permissions_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `role_permissions_ibfk_2` FOREIGN KEY (`module_id`) REFERENCES `modules` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `role_permissions_ibfk_3` FOREIGN KEY (`sub_module_id`) REFERENCES `sub_modules` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `role_permissions_ibfk_4` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `shifts`
--
ALTER TABLE `shifts`
  ADD CONSTRAINT `shifts_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `sub_modules`
--
ALTER TABLE `sub_modules`
  ADD CONSTRAINT `fk_sub_module_module` FOREIGN KEY (`module_id`) REFERENCES `modules` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `system_settings`
--
ALTER TABLE `system_settings`
  ADD CONSTRAINT `system_settings_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `tour_applications`
--
ALTER TABLE `tour_applications`
  ADD CONSTRAINT `tour_applications_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `tour_applications_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `tour_applications_ibfk_3` FOREIGN KEY (`approved_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `users_ibfk_2` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `users_ibfk_3` FOREIGN KEY (`designation_id`) REFERENCES `designations` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `users_ibfk_4` FOREIGN KEY (`reporting_manager_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `users_ibfk_5` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `user_permissions`
--
ALTER TABLE `user_permissions`
  ADD CONSTRAINT `user_permissions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `user_permissions_ibfk_2` FOREIGN KEY (`module_id`) REFERENCES `modules` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `user_permissions_ibfk_3` FOREIGN KEY (`sub_module_id`) REFERENCES `sub_modules` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `user_permissions_ibfk_4` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `user_permissions_ibfk_5` FOREIGN KEY (`granted_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `wfh_applications`
--
ALTER TABLE `wfh_applications`
  ADD CONSTRAINT `wfh_applications_ibfk_1` FOREIGN KEY (`organization_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `wfh_applications_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `wfh_applications_ibfk_3` FOREIGN KEY (`approved_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
