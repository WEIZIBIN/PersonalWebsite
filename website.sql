DROP TABLE IF EXISTS `xiaoice`;
CREATE TABLE `xiaoice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `weibo_username` varchar(45) DEFAULT NULL,
  `weibo_password` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `xiaoice_log`;
CREATE TABLE `xiaoice_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `xiaoice_id` int(11) DEFAULT NULL,
  `msg` varchar(1024) DEFAULT NULL,
  `log_level` varchar(10) DEFAULT NULL,
  `log_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `xiaoice_xiaoice_log_id_idx` (`xiaoice_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;