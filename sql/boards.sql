DROP TABLE IF EXISTS `Board_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Board_type` (
  `type_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `type_sn` varchar(6) DEFAULT NULL,
  PRIMARY KEY (`type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=160 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Board_type`
--

LOCK TABLES `Board_type` WRITE;
/*!40000 ALTER TABLE `Board_type` DISABLE KEYS */;
INSERT INTO `Board_type` VALUES
(10,'Tilemodule B12 Cast','TMB2FC'),
(11,'Tilemodule D8 Cast','TMD8FC'),
(12,'Tilemodule D8 Molded','TMD8FM'),
(13,'Tilemodule G8 Full Cast','TMG8FC'),
(14,'Tilemodule G8 Full Molded','TMG8FM'),
(15,'Tilemodule G8 Right Cast','TMG8RC'),
(16,'Tilemodule G8 Right Molded','TMG8RM'),
(17,'Tilemodule G8 Left Cast','TMG8LC'),
(18,'Tilemodule G8 Left Molded','TMG8LM'),
(19,'Tilemodule G7 Full Cast','TMG7FC'),
(20,'Tilemodule G7 Right Cast','TMG7RC'),
(21,'Tilemodule G7 Left Cast','TMG7LC'),
(22,'Tilemodule G5 Full Cast','TMG5FC'),
(23,'Tilemodule G5 Full Molded','TMG5FM'),
(24,'Tilemodule G5 Right Cast','TMG5RC'),
(25,'Tilemodule G5 Right Molded','TMG5RM'),
(26,'Tilemodule G5 Left Cast','TMG5LC'),
(27,'Tilemodule G5 Left Molded','TMG5LM'),
(28,'Tilemodule G3 Full Cast','TMG3FC'),
(29,'Tilemodule G3 Right Cast','TMG3RC'),
(30,'Tilemodule G3 Left Cast','TMG3LC'),
(40,'ProtoTilemodule B12 Cast','TQB2FC'),
(41,'ProtoTilemodule D8 Cast','TQD8FC'),
(42,'ProtoTilemodule D8 Molded','TQD8FM'),
(43,'ProtoTilemodule G8 Full Cast','TQG8FC'),
(44,'ProtoTilemodule G8 Full Molded','TQG8FM'),
(45,'ProtoTilemodule G8 Right Cast','TQG8RC'),
(46,'ProtoTilemodule G8 Right Molded','TQG8RM'),
(47,'ProtoTilemodule G8 Left Cast','TQG8LC'),
(48,'ProtoTilemodule G8 Left Molded','TQG8LM'),
(49,'ProtoTilemodule G7 Full Cast','TQG7FC'),
(50,'ProtoTilemodule G7 Right Cast','TQG7RC'),
(51,'ProtoTilemodule G7 Left Cast','TQG7LC'),
(52,'ProtoTilemodule G5 Full Cast','TQG5FC'),
(53,'ProtoTilemodule G5 Full Molded','TQG5FM'),
(54,'ProtoTilemodule G5 Right Cast','TQG5RC'),
(55,'ProtoTilemodule G5 Right Molded','TQG5RM'),
(56,'ProtoTilemodule G5 Left Cast','TQG5LC'),
(57,'ProtoTilemodule G5 Left Molded','TQG5LM'),
(58,'ProtoTilemodule G3 Full Cast','TQG3FC'),
(59,'ProtoTilemodule G3 Right Cast','TQG3RC'),
(60,'ProtoTilemodule G3 Left Cast','TQG3LC'),
(100,'TilePCB B12','TBB2F'),
(101,'TilePCB D8','TBD8F'),
(102,'TilePCB G8 Full','TBG8F'),
(103,'TilePCB G8 Right','TBG8R'),
(104,'TilePCB G8 Left','TBG8L'),
(105,'TilePCB G7 Full','TBG7F'),
(106,'TilePCB G7 Right','TBG7R'),
(107,'TilePCB G7 Left','TBG7L'),
(108,'TilePCB G5 Full','TBG5F'),
(109,'TilePCB G5 Right','TBG5R'),
(110,'TilePCB G5 Left','TBG5L'),
(111,'TilePCB G3 Full','TBG3F'),
(112,'TilePCB G3 Right','TBG3R'),
(113,'TilePCB G3 Left','TBG3L');
/*!40000 ALTER TABLE `Board_type` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
