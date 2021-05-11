<!--
 * @Author: CACode
 * @Date: 2021-05-11 17:51:30
-->
# 快速开始
```
pip install cacode_framework
```
## 版本要求
```
python>=3.6
```

# 入门
此框架适用于大部分数据库和web架构，入门门槛需要熟悉python语法即可
## 定义一张表

创建一个名为`demo`数据库  
使用mysql命令行工具或者navicat执行以下sql语句，推荐使用navicat

```
CREATE DATABASE demo
```

然后创建一张名为`demo_table`的表
```
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `demo_table`;
CREATE TABLE `demo_table`  (
  `t_id` int NOT NULL AUTO_INCREMENT,
  `t_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `t_pwd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `t_msg` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`t_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1000000 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;

```