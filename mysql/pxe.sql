/*
MySQL Data Transfer
Source Host: localhost
Source Database: pxe
Target Host: localhost
Target Database: pxe
Date: 2011/6/25 21:57:10
*/

SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for os
-- ----------------------------
DROP TABLE IF EXISTS `os`;
CREATE TABLE `os` (
  `id` int(11) NOT NULL auto_increment,
  `distro` varchar(300) default 'CentOS',
  `releasever` varchar(300) default '6.0',
  `basearch` varchar(300) default 'x86_64',
  `createtime` datetime default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records 
-- ----------------------------
INSERT INTO `os` VALUES ('00001','CentOS', '6.1', 'x86_64', '2011-06-03 06:08:10');
INSERT INTO `os` VALUES ('00002','CentOS', '6.2', 'x86_64', '2011-06-03 06:08:10');
INSERT INTO `os` VALUES ('00003','CentOS', '6.3', 'x86_64', '2011-06-03 06:08:10');
INSERT INTO `os` VALUES ('00004','CentOS', '6.4', 'x86_64', '2011-06-03 06:08:10');
INSERT INTO `os` VALUES ('00005','CentOS', '6.5', 'x86_64', '2011-06-04 23:01:31');
