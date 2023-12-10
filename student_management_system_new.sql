/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80032 (8.0.32)
 Source Host           : localhost:3306
 Source Schema         : student_management_system

 Target Server Type    : MySQL
 Target Server Version : 80032 (8.0.32)
 File Encoding         : 65001

 Date: 22/11/2023 12:59:08
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL COMMENT '课程名称',
  `sort` varchar(255) COLLATE utf8mb4_general_ci NOT NULL COMMENT '排序',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of course
-- ----------------------------
BEGIN;
INSERT INTO `course` (`id`, `course_name`, `sort`, `created_time`, `updated_time`) VALUES (1, 'Computer', '0', NULL, '2023-11-22 03:41:10');
INSERT INTO `course` (`id`, `course_name`, `sort`, `created_time`, `updated_time`) VALUES (2, 'Chinese', '0', '2023-11-21 12:58:36', '2023-11-22 03:40:35');
INSERT INTO `course` (`id`, `course_name`, `sort`, `created_time`, `updated_time`) VALUES (5, 'English', '0', '2023-11-21 13:05:05', '2023-11-22 03:41:02');
INSERT INTO `course` (`id`, `course_name`, `sort`, `created_time`, `updated_time`) VALUES (6, 'mathematics', '0', '2023-11-22 03:40:50', '2023-11-22 03:40:50');
COMMIT;

-- ----------------------------
-- Table structure for student_score
-- ----------------------------
DROP TABLE IF EXISTS `student_score`;
CREATE TABLE `student_score` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL COMMENT '学生ID',
  `teacher_id` int NOT NULL COMMENT '老师ID',
  `course_id` int NOT NULL COMMENT '课程',
  `course_name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '课程名称',
  `grade` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '作业分数',
  `midterm_exam_score` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '期中考试分数',
  `final_exam_score` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '期末考试成绩',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `course_id` (`course_id`),
  KEY `uid` (`student_id`),
  KEY `tid` (`teacher_id`),
  CONSTRAINT `student_score_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`),
  CONSTRAINT `student_score_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student_user` (`id`),
  CONSTRAINT `student_score_ibfk_3` FOREIGN KEY (`teacher_id`) REFERENCES `teacher_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of student_score
-- ----------------------------
BEGIN;
INSERT INTO `student_score` (`id`, `student_id`, `teacher_id`, `course_id`, `course_name`, `grade`, `midterm_exam_score`, `final_exam_score`, `created_time`, `updated_time`) VALUES (1, 1, 2, 1, '计算机1', '100', '100', '100', NULL, NULL);
INSERT INTO `student_score` (`id`, `student_id`, `teacher_id`, `course_id`, `course_name`, `grade`, `midterm_exam_score`, `final_exam_score`, `created_time`, `updated_time`) VALUES (6, 1, 2, 2, '语文', '90', '99', '90', '2023-11-21 16:28:00', '2023-11-21 16:28:00');
INSERT INTO `student_score` (`id`, `student_id`, `teacher_id`, `course_id`, `course_name`, `grade`, `midterm_exam_score`, `final_exam_score`, `created_time`, `updated_time`) VALUES (7, 1, 2, 5, 'English', '98', '89', '87', '2023-11-21 16:28:14', '2023-11-22 03:54:46');
INSERT INTO `student_score` (`id`, `student_id`, `teacher_id`, `course_id`, `course_name`, `grade`, `midterm_exam_score`, `final_exam_score`, `created_time`, `updated_time`) VALUES (8, 3, 5, 1, 'Computer', '100', '99', '98', '2023-11-22 03:53:58', '2023-11-22 03:53:58');
INSERT INTO `student_score` (`id`, `student_id`, `teacher_id`, `course_id`, `course_name`, `grade`, `midterm_exam_score`, `final_exam_score`, `created_time`, `updated_time`) VALUES (9, 3, 5, 2, 'Chinese', '100', '97', '98', '2023-11-22 03:54:11', '2023-11-22 03:54:11');
INSERT INTO `student_score` (`id`, `student_id`, `teacher_id`, `course_id`, `course_name`, `grade`, `midterm_exam_score`, `final_exam_score`, `created_time`, `updated_time`) VALUES (10, 3, 5, 5, 'English', '100', '100', '100', '2023-11-22 03:54:19', '2023-11-22 03:54:19');
INSERT INTO `student_score` (`id`, `student_id`, `teacher_id`, `course_id`, `course_name`, `grade`, `midterm_exam_score`, `final_exam_score`, `created_time`, `updated_time`) VALUES (11, 3, 5, 6, 'mathematics', '89', '98', '96', '2023-11-22 03:54:28', '2023-11-22 03:54:28');
INSERT INTO `student_score` (`id`, `student_id`, `teacher_id`, `course_id`, `course_name`, `grade`, `midterm_exam_score`, `final_exam_score`, `created_time`, `updated_time`) VALUES (12, 1, 5, 6, 'mathematics', '100', '99', '97', '2023-11-22 03:54:56', '2023-11-22 03:54:56');
COMMIT;

-- ----------------------------
-- Table structure for student_user
-- ----------------------------
DROP TABLE IF EXISTS `student_user`;
CREATE TABLE `student_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `account` varchar(255) COLLATE utf8mb4_general_ci NOT NULL COMMENT '账户名',
  `password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL COMMENT '账户密码',
  `phone` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '手机号',
  `email` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '用户邮箱',
  `student_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '学号',
  `address` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '详细地址',
  `emergency_contact` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '紧急联系人',
  `emergency_phone` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '紧急联系人电话',
  `security_issues` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '安全问题',
  `security_answer` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '安全问题答案',
  `major` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '专业',
  `user_type` int(1) unsigned zerofill NOT NULL COMMENT '用户类型 0学生 1教师 2管理员',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of student_user
-- ----------------------------
BEGIN;
INSERT INTO `student_user` (`id`, `account`, `password`, `phone`, `email`, `student_id`, `address`, `emergency_contact`, `emergency_phone`, `security_issues`, `security_answer`, `major`, `user_type`, `created_time`, `updated_time`) VALUES (1, 'student1', 'rGyqSvdqx9qhydWdQEpuPg==', '13666666666', '123123@qq.com', '1', 'No. 9 Zhongshan Avenue', 'Li Ming', '13711111111', 'Testing issues', 'rGyqSvdqx9qhydWdQEpuPg==', 'computer', 0, '2023-11-21 06:40:59', '2023-11-22 04:04:37');
INSERT INTO `student_user` (`id`, `account`, `password`, `phone`, `email`, `student_id`, `address`, `emergency_contact`, `emergency_phone`, `security_issues`, `security_answer`, `major`, `user_type`, `created_time`, `updated_time`) VALUES (3, 'student2', 'rGyqSvdqx9qhydWdQEpuPg==', '13766666666', 'student2@qq.com', '2', 'No. 8 Zhongshan Avenue', 'Xiao Hong', '13988888888', 'Testing issues', 'rGyqSvdqx9qhydWdQEpuPg==', 'Chinese', 0, '2023-11-22 03:49:05', '2023-11-22 03:51:53');
COMMIT;

-- ----------------------------
-- Table structure for teacher_user
-- ----------------------------
DROP TABLE IF EXISTS `teacher_user`;
CREATE TABLE `teacher_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `account` varchar(255) COLLATE utf8mb4_general_ci NOT NULL COMMENT '账户',
  `password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL COMMENT '密码',
  `phone` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '手机号',
  `email` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '邮箱',
  `user_name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '用户名',
  `college` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '学院',
  `gender` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '性别',
  `user_type` int NOT NULL DEFAULT '1' COMMENT '用户类型 0学生 1教师 2管理员',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of teacher_user
-- ----------------------------
BEGIN;
INSERT INTO `teacher_user` (`id`, `account`, `password`, `phone`, `email`, `user_name`, `college`, `gender`, `user_type`, `created_time`, `updated_time`) VALUES (2, 'teacher2', 'JnLpcfDlBIrSu7JrN45VsIk+upPHhjG/fLjBW9/VNA4=', '13888888888', 'teacher2@test.com', 'teacher2', 'school of computing', '1', 1, '2023-11-21 10:40:53', '2023-11-22 03:37:53');
INSERT INTO `teacher_user` (`id`, `account`, `password`, `phone`, `email`, `user_name`, `college`, `gender`, `user_type`, `created_time`, `updated_time`) VALUES (5, 'teacher1', 'rGyqSvdqx9qhydWdQEpuPg==', '13666666666', 'test@qq.com', 'teacher1', 'college of humanities', '0', 1, '2023-11-22 03:39:18', '2023-11-22 03:39:18');
COMMIT;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `account` varchar(255) COLLATE utf8mb4_general_ci NOT NULL COMMENT '账号',
  `password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL COMMENT '密码',
  `phone` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '手机号',
  `email` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '邮箱',
  `user_name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '用户名',
  `user_type` int NOT NULL DEFAULT '2' COMMENT '用户类型 0学生 1教师 2管理员',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of user
-- ----------------------------
BEGIN;
INSERT INTO `user` (`id`, `account`, `password`, `phone`, `email`, `user_name`, `user_type`, `created_time`, `updated_time`) VALUES (1, 'administrator', 'rGyqSvdqx9qhydWdQEpuPg==', '13666666666', 'admin@test.com', 'administrator', 2, '2023-11-21 12:52:28', '2023-11-21 12:52:31');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
