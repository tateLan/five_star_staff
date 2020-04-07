CREATE DATABASE  IF NOT EXISTS `five_star` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `five_star`;
-- MySQL dump 10.13  Distrib 8.0.19, for Linux (x86_64)
--
-- Host: vps721220.ovh.net    Database: five_star
-- ------------------------------------------------------
-- Server version	8.0.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `client` (
  `client_id` int(11) NOT NULL,
  `telegram_username` text,
  `first_name` text,
  `middle_name` text,
  `last_name` text,
  `company` text,
  `phone` varchar(20) DEFAULT NULL,
  `email` text,
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client`
--

LOCK TABLES `client` WRITE;
/*!40000 ALTER TABLE `client` DISABLE KEYS */;
INSERT INTO `client` VALUES (345763058,'@OlekSeyy','Олексій','Васильович','Назарчук','НУБЕЕЕЕЕП','+380977240216','alexey.nazarchuk@gmail.com');
/*!40000 ALTER TABLE `client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `config`
--

DROP TABLE IF EXISTS `config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `config` (
  `_key` varchar(50) NOT NULL,
  `_value` varchar(50) NOT NULL,
  PRIMARY KEY (`_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `config`
--

LOCK TABLES `config` WRITE;
/*!40000 ALTER TABLE `config` DISABLE KEYS */;
INSERT INTO `config` VALUES ('CHECK_IN_ALLOWED_BEFORE_SHIFT_MIN','15'),('HOURS_BETWEEN_SHIFTS','6'),('MID_RATE','75'),('NEW_RATE','50'),('PRICE_OF_KM','3'),('PRO_RATE','100'),('STAT_ITEMS_ON_ONE_PAGE','10'),('TIME_TRACKER_SECONDS_PERIOD','600');
/*!40000 ALTER TABLE `config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event` (
  `event_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_request_id` int(11) NOT NULL,
  `title` varchar(20) DEFAULT NULL,
  `location` varchar(65) DEFAULT NULL,
  `date_starts` datetime NOT NULL,
  `date_ends` datetime NOT NULL,
  `event_type_id` int(11) DEFAULT NULL,
  `event_class_id` int(11) DEFAULT NULL,
  `number_of_guests` int(11) NOT NULL,
  `staff_needed` int(11) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `feedback` int(11) DEFAULT NULL,
  PRIMARY KEY (`event_id`),
  KEY `R_26` (`event_class_id`),
  KEY `R_27` (`event_type_id`),
  KEY `R_23` (`event_request_id`),
  CONSTRAINT `event_ibfk_1` FOREIGN KEY (`event_class_id`) REFERENCES `event_class` (`event_class_id`),
  CONSTRAINT `event_ibfk_2` FOREIGN KEY (`event_type_id`) REFERENCES `event_type` (`event_type_id`),
  CONSTRAINT `event_ibfk_3` FOREIGN KEY (`event_request_id`) REFERENCES `event_request` (`event_request_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES (1,1,'some test event','latitude:50.387142 longitude:30.477375','2020-04-07 15:00:00','2020-04-07 15:20:00',3,2,10,2,93.85,NULL);
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_class`
--

DROP TABLE IF EXISTS `event_class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_class` (
  `event_class_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_class_name` varchar(20) DEFAULT NULL,
  `guests_per_waiter` int(11) DEFAULT NULL,
  PRIMARY KEY (`event_class_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_class`
--

LOCK TABLES `event_class` WRITE;
/*!40000 ALTER TABLE `event_class` DISABLE KEYS */;
INSERT INTO `event_class` VALUES (1,'Найвищий',3),(2,'Високий',5),(3,'Середній',7),(4,'Початковий',10);
/*!40000 ALTER TABLE `event_class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_request`
--

DROP TABLE IF EXISTS `event_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_request` (
  `event_request_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `date_registered` datetime NOT NULL,
  `staff_processed` int(11) DEFAULT NULL,
  `processed` tinyint(1) NOT NULL,
  PRIMARY KEY (`event_request_id`),
  KEY `R_24` (`client_id`),
  KEY `R_25` (`staff_processed`),
  CONSTRAINT `event_request_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`client_id`),
  CONSTRAINT `event_request_ibfk_2` FOREIGN KEY (`staff_processed`) REFERENCES `staff` (`staff_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_request`
--

LOCK TABLES `event_request` WRITE;
/*!40000 ALTER TABLE `event_request` DISABLE KEYS */;
INSERT INTO `event_request` VALUES (1,345763058,'2020-04-04 14:33:12',116516979,1);
/*!40000 ALTER TABLE `event_request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_type`
--

DROP TABLE IF EXISTS `event_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_type` (
  `event_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_type_name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`event_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_type`
--

LOCK TABLES `event_type` WRITE;
/*!40000 ALTER TABLE `event_type` DISABLE KEYS */;
INSERT INTO `event_type` VALUES (1,'День народження'),(2,'Весілля'),(3,'Корпоратив');
/*!40000 ALTER TABLE `event_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `qualification`
--

DROP TABLE IF EXISTS `qualification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `qualification` (
  `qualification_id` int(11) NOT NULL AUTO_INCREMENT,
  `qualification_name` text,
  PRIMARY KEY (`qualification_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `qualification`
--

LOCK TABLES `qualification` WRITE;
/*!40000 ALTER TABLE `qualification` DISABLE KEYS */;
INSERT INTO `qualification` VALUES (1,'Професіонал'),(2,'Середній рівень'),(3,'Початківець'),(4,'Не підтверджено');
/*!40000 ALTER TABLE `qualification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `qualification_confirmation`
--

DROP TABLE IF EXISTS `qualification_confirmation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `qualification_confirmation` (
  `qualification_confirmation_id` int(11) NOT NULL AUTO_INCREMENT,
  `qualification_id` int(11) NOT NULL,
  `date_placed` datetime NOT NULL,
  `date_approved` datetime DEFAULT NULL,
  `confirmed` tinyint(1) NOT NULL,
  PRIMARY KEY (`qualification_confirmation_id`),
  KEY `R_31` (`qualification_id`),
  CONSTRAINT `qualification_confirmation_ibfk_1` FOREIGN KEY (`qualification_id`) REFERENCES `qualification` (`qualification_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `qualification_confirmation`
--

LOCK TABLES `qualification_confirmation` WRITE;
/*!40000 ALTER TABLE `qualification_confirmation` DISABLE KEYS */;
INSERT INTO `qualification_confirmation` VALUES (2,1,'2020-04-03 20:03:49','2020-04-03 20:03:50',1),(5,1,'2020-04-07 14:21:47','2020-04-07 14:23:00',1);
/*!40000 ALTER TABLE `qualification_confirmation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `role_id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` text,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'Адміністратор'),(2,'Менеджер'),(3,'Офіціант'),(4,'Не підтверджено');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_confirmation`
--

DROP TABLE IF EXISTS `role_confirmation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role_confirmation` (
  `role_confirmation_id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) NOT NULL,
  `date_placed` datetime NOT NULL,
  `date_approved` datetime DEFAULT NULL,
  `confirmed` tinyint(1) NOT NULL,
  PRIMARY KEY (`role_confirmation_id`),
  KEY `R_30` (`role_id`),
  CONSTRAINT `role_confirmation_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_confirmation`
--

LOCK TABLES `role_confirmation` WRITE;
/*!40000 ALTER TABLE `role_confirmation` DISABLE KEYS */;
INSERT INTO `role_confirmation` VALUES (6,2,'2020-04-03 20:03:46','2020-04-03 20:03:47',1),(9,3,'2020-04-07 14:21:42','2020-04-07 14:23:00',1);
/*!40000 ALTER TABLE `role_confirmation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shift`
--

DROP TABLE IF EXISTS `shift`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shift` (
  `shift_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) DEFAULT NULL,
  `professionals_number` int(11) NOT NULL,
  `middles_number` int(11) NOT NULL,
  `beginers_number` int(11) NOT NULL,
  `supervisor` int(11) DEFAULT NULL,
  `ended` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`shift_id`),
  KEY `R_34` (`supervisor`),
  KEY `R_41` (`event_id`),
  CONSTRAINT `shift_ibfk_1` FOREIGN KEY (`supervisor`) REFERENCES `staff` (`staff_id`),
  CONSTRAINT `shift_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `event` (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shift`
--

LOCK TABLES `shift` WRITE;
/*!40000 ALTER TABLE `shift` DISABLE KEYS */;
INSERT INTO `shift` VALUES (1,1,2,0,0,898773475,1);
/*!40000 ALTER TABLE `shift` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shift_registration`
--

DROP TABLE IF EXISTS `shift_registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shift_registration` (
  `shift_registration_id` int(11) NOT NULL AUTO_INCREMENT,
  `shift_id` int(11) NOT NULL,
  `staff_id` int(11) NOT NULL,
  `registered` tinyint(4) DEFAULT '1',
  `date_registered` datetime NOT NULL,
  `check_in` datetime DEFAULT NULL,
  `check_out` datetime DEFAULT NULL,
  `rating` float DEFAULT NULL,
  `payment` float DEFAULT NULL,
  PRIMARY KEY (`shift_registration_id`),
  KEY `R_36` (`shift_id`),
  KEY `R_37` (`staff_id`),
  CONSTRAINT `shift_registration_ibfk_1` FOREIGN KEY (`shift_id`) REFERENCES `shift` (`shift_id`),
  CONSTRAINT `shift_registration_ibfk_2` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`staff_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shift_registration`
--

LOCK TABLES `shift_registration` WRITE;
/*!40000 ALTER TABLE `shift_registration` DISABLE KEYS */;
INSERT INTO `shift_registration` VALUES (2,1,898773475,1,'2020-04-07 14:42:00','2020-04-07 14:46:00','2020-04-07 15:45:00',NULL,NULL),(3,1,123,1,'2020-04-07 14:42:00','2020-04-07 14:46:01','2020-04-07 15:44:00',4,54.1194);
/*!40000 ALTER TABLE `shift_registration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `staff_id` int(11) NOT NULL,
  `first_name` text,
  `middle_name` text,
  `last_name` text,
  `qualification_confirmation_id` int(11) DEFAULT NULL,
  `role_confirmation_id` int(11) DEFAULT NULL,
  `rating` float DEFAULT NULL,
  `date_registered` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `events_done` int(11) DEFAULT NULL,
  `rate` int(11) DEFAULT NULL,
  PRIMARY KEY (`staff_id`),
  KEY `R_28` (`qualification_confirmation_id`),
  KEY `R_29` (`role_confirmation_id`),
  CONSTRAINT `staff_ibfk_1` FOREIGN KEY (`qualification_confirmation_id`) REFERENCES `qualification_confirmation` (`qualification_confirmation_id`),
  CONSTRAINT `staff_ibfk_2` FOREIGN KEY (`role_confirmation_id`) REFERENCES `role_confirmation` (`role_confirmation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES (123,'tony','hovard','stark',5,9,4,'2020-04-07 13:20:28',1,50),(116516979,'Ілля','Олегович','Танасюк',2,6,0,'2020-04-03 19:02:35',0,50),(898773475,'Наталія','Василівна','Танасюк',5,9,0,'2020-04-07 13:20:27',0,50);
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff_last_message_to_edit`
--

DROP TABLE IF EXISTS `staff_last_message_to_edit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff_last_message_to_edit` (
  `staff_id` int(11) NOT NULL,
  `message_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`staff_id`),
  CONSTRAINT `staff_last_message_to_edit_ibfk_1` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`staff_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff_last_message_to_edit`
--

LOCK TABLES `staff_last_message_to_edit` WRITE;
/*!40000 ALTER TABLE `staff_last_message_to_edit` DISABLE KEYS */;
INSERT INTO `staff_last_message_to_edit` VALUES (116516979,1011),(898773475,971);
/*!40000 ALTER TABLE `staff_last_message_to_edit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'five_star'
--

--
-- Dumping routines for database 'five_star'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-07 21:40:10
