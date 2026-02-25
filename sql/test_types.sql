--
-- LOAD ME AFTER LOADING BOARD_TYPES
--

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Test_Type`
--

DROP TABLE IF EXISTS `Test_Type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Test_Type` (
  `test_type` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  `required` tinyint(1) NOT NULL,
  `desc_short` varchar(50) DEFAULT NULL,
  `desc_long` varchar(250) DEFAULT NULL,
  `relative_order` int(11) NOT NULL,
  PRIMARY KEY (`test_type`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Test_Type`
--

LOCK TABLES `Test_Type` WRITE;
/*!40000 ALTER TABLE `Test_Type` DISABLE KEYS */;
INSERT INTO `Test_Type` VALUES
(1,'Registered',0,'Register board in central DB','Passed if board has been registered, failed if we do not want to register the board',999),
(2,'Visual Inspection',1,'Preliminary check of board','Check that all components are present on board and that there is no visible damage',0),
(3,'Thermal Cycle',1,'Has gone through the thermal chamber','Thermal cycled the board down to -40C and then back up to room temperature to check if any mechanical failures show up',10),
(4,'Reception QC',1,'Check that the board communicates','Perform the pedestal and LED tests on the received boards and make sure that nothing changed during shipping since Maryland tested the boards',1),
(5,'Cosmic Stand',1,'Has been tested in the cosmic stand','The Tile Module is put into the cosmic test stand and run for 2 days. This checks statistics on light yield and serves as an electric systems check',11);
/*!40000 ALTER TABLE `Test_Type` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

DROP TABLE IF EXISTS `Type_test_stitch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Type_test_stitch` (
  `type_id` int(10) unsigned DEFAULT NULL,
  `test_type_id` int(10) unsigned DEFAULT NULL,
  KEY `type_id` (`type_id`),
  KEY `test_type_id` (`test_type_id`)
);

LOCK TABLES `Type_test_stitch` WRITE;

--
-- Link registered to all tile modules
-- 
INSERT INTO `Type_test_stitch` VALUES
(10,1),(11,1),(12,1),(13,1),(14,1),(15,1),(16,1),(17,1),(18,1),(19,1),
(20,1),(21,1),(22,1),(23,1),(24,1),(25,1),(26,1),(27,1),(28,1),(29,1),
(30,1);

--
-- Link visual inspection to all tile PCBs
-- 
INSERT INTO `Type_test_stitch` VALUES
(100,2),(101,2),(102,2),(103,2),(104,2),(105,2),(106,2),(107,2),(108,2),(109,2),
(110,2),(111,2),(112,2),(113,2);
--
-- Link visual inspection to all protomodules
-- 
INSERT INTO `Type_test_stitch` VALUES
(40,2),(41,2),(42,2),(43,2),(44,2),(45,2),(46,2),(47,2),(48,2),(49,2),
(50,2),(51,2),(52,2),(53,2),(54,2),(55,2),(56,2),(57,2),(58,2),(59,2),
(60,2);

--
-- Link thermal cycle to all tile modules
-- 
INSERT INTO `Type_test_stitch` VALUES
(10,3),(11,3),(12,3),(13,3),(14,3),(15,3),(16,3),(17,3),(18,3),(19,3),
(20,3),(21,3),(22,3),(23,3),(24,3),(25,3),(26,3),(27,3),(28,3),(29,3),
(30,3);

--
-- Link reception QC to all tile PCBs
-- 
INSERT INTO `Type_test_stitch` VALUES
(100,4),(101,4),(102,4),(103,4),(104,4),(105,4),(106,4),(107,4),(108,4),(109,4),
(110,4),(111,4),(112,4),(113,4);

--
-- Link cosmic stand to all tile modules
-- 
INSERT INTO `Type_test_stitch` VALUES
(10,5),(11,5),(12,5),(13,5),(14,5),(15,5),(16,5),(17,5),(18,5),(19,5),
(20,5),(21,5),(22,5),(23,5),(24,5),(25,5),(26,5),(27,5),(28,5),(29,5),
(30,5);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
