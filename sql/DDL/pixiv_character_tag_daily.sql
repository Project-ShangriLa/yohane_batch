CREATE TABLE `pixiv_character_tag_daily` (
  `bases_id` int(11) DEFAULT NULL,
  `character_id` int(11) DEFAULT NULL,
  `get_date` datetime DEFAULT NULL,
  `search_word` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `total` int(11) DEFAULT NULL,
  `note` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `json` text COLLATE utf8_unicode_ci,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  KEY `pixiv_tag_character_daily_base_id_index` (`bases_id`),
  KEY `pixiv_tag_character_daily_base_id_and_get_date_index` (`bases_id`,`get_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;