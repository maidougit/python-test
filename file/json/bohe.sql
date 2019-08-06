CREATE TABLE `bohejiankang` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `food_id` int(11) DEFAULT NULL,
  `calory` decimal(6,2) DEFAULT NULL COMMENT '卡路里',
  `weight` decimal(6,2) DEFAULT NULL COMMENT '克',
  `code` varchar(255) DEFAULT NULL COMMENT 'code码，获取json',
  `name` varchar(255) DEFAULT NULL COMMENT '民名称',
  `thumb_image_name` varchar(1024) DEFAULT NULL COMMENT '缩略图',
  `health_light` tinyint(1) DEFAULT NULL,
  `is_liquid` varchar(255) DEFAULT NULL COMMENT '是否是液体',
  `food_detail` json DEFAULT NULL COMMENT '食物详情',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;

