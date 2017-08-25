DROP TABLE IF EXISTS `xiaoice`;
CREATE TABLE `xiaoice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `weibo_username` varchar(45) DEFAULT NULL,
  `weibo_password` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;