/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80020
 Source Host           : localhost:3306
 Source Schema         : demo

 Target Server Type    : MySQL
 Target Server Version : 80020
 File Encoding         : 65001

 Date: 08/03/2021 14:27:30
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for demo_table
-- ----------------------------
DROP TABLE IF EXISTS `demo_table`;
CREATE TABLE `demo_table`  (
  `index` int NOT NULL,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `selects` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `success` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`index`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of demo_table
-- ----------------------------
INSERT INTO `demo_table` VALUES (0, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (1, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (2, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (3, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (4, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (5, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (6, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (7, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (8, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (9, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (10, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (11, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (12, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (13, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (14, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (15, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (16, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (17, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (18, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (19, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (20, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (21, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (22, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (23, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (24, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (25, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (26, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (27, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (28, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (29, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (30, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (31, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (32, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (33, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (34, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (35, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (36, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (37, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (38, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (39, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (40, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (41, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (42, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (43, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (44, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (45, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (46, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (47, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (48, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (49, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (50, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (51, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (52, 'test title', 'test selects', 'false');
INSERT INTO `demo_table` VALUES (53, 'test title', 'test selects', 'false');

SET FOREIGN_KEY_CHECKS = 1;
