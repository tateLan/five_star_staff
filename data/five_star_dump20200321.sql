CREATE DATABASE  IF NOT EXISTS `five_star_db` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `five_star_db`;
-- MySQL dump 10.13  Distrib 8.0.19, for Linux (x86_64)
--
-- Host: vps721220.ovh.net    Database: five_star_db
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
-- Table structure for table `clients`
--

DROP TABLE IF EXISTS `clients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clients` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `telegram_username` varchar(45) DEFAULT NULL,
  `first_name` varchar(40) DEFAULT NULL,
  `last_name` varchar(40) DEFAULT NULL,
  `company` varchar(40) DEFAULT NULL,
  `phone` varchar(13) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients`
--

LOCK TABLES `clients` WRITE;
/*!40000 ALTER TABLE `clients` DISABLE KEYS */;
INSERT INTO `clients` VALUES (1,'illia_tanasiuk','Illia','Tanasiuk','nubeeeeep','+380673658854','illya.tanasyuk@gmail.com');
/*!40000 ALTER TABLE `clients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `curency`
--

DROP TABLE IF EXISTS `curency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `curency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_of_curency` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `curency`
--

LOCK TABLES `curency` WRITE;
/*!40000 ALTER TABLE `curency` DISABLE KEYS */;
INSERT INTO `curency` VALUES (1,'uah'),(2,'usd'),(3,'eur'),(4,'pln');
/*!40000 ALTER TABLE `curency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_class`
--

DROP TABLE IF EXISTS `event_class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_class` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `class` varchar(25) DEFAULT NULL,
  `guests_per_waiter` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_class`
--

LOCK TABLES `event_class` WRITE;
/*!40000 ALTER TABLE `event_class` DISABLE KEYS */;
INSERT INTO `event_class` VALUES (1,'найвищий',3),(2,'високий',5),(3,'середній',7),(4,'початковий',10);
/*!40000 ALTER TABLE `event_class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_request`
--

DROP TABLE IF EXISTS `event_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_request` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) DEFAULT NULL,
  `date_registered` date NOT NULL,
  `staff_processed` int(11) DEFAULT NULL,
  `processed` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_request`
--

LOCK TABLES `event_request` WRITE;
/*!40000 ALTER TABLE `event_request` DISABLE KEYS */;
INSERT INTO `event_request` VALUES (1,1,'2020-01-25',116516979,1),(2,1,'2020-02-12',123,1),(3,1,'2020-03-01',116516979,1),(4,1,'2020-03-17',116516979,1);
/*!40000 ALTER TABLE `event_request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_types`
--

DROP TABLE IF EXISTS `event_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_of_event` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_types`
--

LOCK TABLES `event_types` WRITE;
/*!40000 ALTER TABLE `event_types` DISABLE KEYS */;
INSERT INTO `event_types` VALUES (1,'весілля'),(2,'день народження'),(3,'корпоратив');
/*!40000 ALTER TABLE `event_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_request_id` int(11) DEFAULT NULL,
  `title` varchar(60) DEFAULT NULL,
  `location` varchar(40) DEFAULT NULL,
  `date_starts` datetime NOT NULL,
  `date_ends` datetime NOT NULL,
  `guests` int(11) NOT NULL,
  `type_of_event` int(11) DEFAULT NULL,
  `event_class` int(11) DEFAULT NULL,
  `staff_needed` int(11) DEFAULT NULL,
  `price` decimal(10,0) DEFAULT NULL,
  `curency` int(11) DEFAULT NULL,
  `feedback` decimal(10,0) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` VALUES (1,1,'др румянцева','latitude:54.453478 longitude:17.043673','2020-02-28 21:00:00','2020-02-29 05:00:00',10,2,1,4,6253,1,NULL),(2,2,'qweert','lat','2020-02-25 19:00:00','2020-02-28 10:00:00',1,2,1,4,6526,1,5),(3,3,'для мілих дам','latitude:54.453478 longitude:17.043673','2020-03-07 13:58:00','2020-03-08 14:30:00',10,3,1,4,5053,1,NULL),(4,4,'idk some fcking event','latitude:54.453478 longitude:17.043673','2020-03-18 17:32:00','2020-03-18 17:35:00',10,3,1,4,4653,1,NULL);
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `qualification`
--

DROP TABLE IF EXISTS `qualification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `qualification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `degree` varchar(25) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `qualification`
--

LOCK TABLES `qualification` WRITE;
/*!40000 ALTER TABLE `qualification` DISABLE KEYS */;
INSERT INTO `qualification` VALUES (1,'професіонал'),(2,'середній рівень'),(3,'початківець'),(4,'не підтверджено');
/*!40000 ALTER TABLE `qualification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `qualification_confirmation`
--

DROP TABLE IF EXISTS `qualification_confirmation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `qualification_confirmation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `staff_id` int(11) DEFAULT NULL,
  `requested_qualification` int(11) DEFAULT NULL,
  `date_placed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_confirmed` datetime DEFAULT NULL,
  `confirmed_by` int(11) DEFAULT NULL,
  `confirmed` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `qualification_confirmation`
--

LOCK TABLES `qualification_confirmation` WRITE;
/*!40000 ALTER TABLE `qualification_confirmation` DISABLE KEYS */;
INSERT INTO `qualification_confirmation` VALUES (6,1165169791,1,'2019-09-21 14:49:14','2019-09-21 16:49:15',116516979,1),(14,123,3,'2020-02-02 16:20:12','2020-02-02 17:29:00',116516979,1),(18,345763058,1,'2020-02-16 10:59:47','2020-02-16 12:00:00',116516979,1);
/*!40000 ALTER TABLE `qualification_confirmation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_confirmation`
--

DROP TABLE IF EXISTS `role_confirmation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role_confirmation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `staff_id` int(11) DEFAULT NULL,
  `requested_role` int(11) DEFAULT NULL,
  `date_placed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_confirmed` datetime DEFAULT NULL,
  `confirmed_by` int(11) DEFAULT NULL,
  `confirmed` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_confirmation`
--

LOCK TABLES `role_confirmation` WRITE;
/*!40000 ALTER TABLE `role_confirmation` DISABLE KEYS */;
INSERT INTO `role_confirmation` VALUES (17,1165169791,1,'2019-09-21 14:49:13','2019-09-21 16:49:14',116516979,1),(27,123,2,'2020-01-21 17:18:41','2020-01-25 17:06:00',116516979,1),(33,345763058,1,'2020-02-16 10:59:45','2020-02-16 12:00:00',116516979,1);
/*!40000 ALTER TABLE `role_confirmation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id_role` int(11) NOT NULL AUTO_INCREMENT,
  `name_role` varchar(35) NOT NULL,
  PRIMARY KEY (`id_role`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'адміністратор'),(2,'офіціант'),(3,'менеджер'),(4,'не підтверджено');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shift`
--

DROP TABLE IF EXISTS `shift`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shift` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) NOT NULL,
  `profesionals_number` int(11) NOT NULL,
  `middles_number` int(11) NOT NULL,
  `beginers_number` int(11) NOT NULL,
  `supervisor` int(11) DEFAULT NULL,
  `ended` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_shift_1_idx` (`supervisor`),
  CONSTRAINT `fk_shift_1` FOREIGN KEY (`supervisor`) REFERENCES `staff` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shift`
--

LOCK TABLES `shift` WRITE;
/*!40000 ALTER TABLE `shift` DISABLE KEYS */;
INSERT INTO `shift` VALUES (5,2,4,0,0,123,1),(6,3,4,0,0,116516979,1),(7,4,4,0,0,116516979,1);
/*!40000 ALTER TABLE `shift` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shift_registration`
--

DROP TABLE IF EXISTS `shift_registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shift_registration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `shift_id` int(11) NOT NULL,
  `staff_id` int(11) NOT NULL,
  `date_registered` datetime NOT NULL,
  `registered` tinyint(1) NOT NULL,
  `check_in` datetime DEFAULT NULL,
  `check_out` datetime DEFAULT NULL,
  `rating` decimal(10,0) DEFAULT NULL,
  `payment` decimal(10,0) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shift_registration`
--

LOCK TABLES `shift_registration` WRITE;
/*!40000 ALTER TABLE `shift_registration` DISABLE KEYS */;
INSERT INTO `shift_registration` VALUES (31,6,116516979,'2020-03-07 13:55:00',1,'2020-03-07 13:55:00','2020-03-08 14:31:00',NULL,NULL),(43,7,116516979,'2020-03-18 17:31:00',1,'2020-03-18 17:31:00','2020-03-18 17:50:00',NULL,NULL),(44,7,345763058,'2020-03-18 17:31:00',1,'2020-03-18 17:31:00','2020-03-18 17:36:00',5,5);
/*!40000 ALTER TABLE `shift_registration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `id` int(11) NOT NULL,
  `first_name` varchar(40) DEFAULT NULL,
  `middle_name` varchar(40) DEFAULT NULL,
  `last_name` varchar(40) DEFAULT NULL,
  `staff_role` int(11) DEFAULT NULL,
  `qualification` int(11) DEFAULT NULL,
  `current_rating` float DEFAULT '0',
  `general_rating` float DEFAULT '0',
  `registration_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `events_done` int(11) DEFAULT '0',
  `rate` decimal(10,0) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES (123,'tony','hovard','stark',3,1,0,0,'2020-01-21 17:18:00',0,50),(116516979,'Ілля','Олегович','Танасюк',2,1,0,0,'2019-09-21 14:49:03',0,50),(345763058,'Ігнат','Васильович','Іванов',1,1,5,0,'2020-02-16 10:59:29',1,50);
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'five_star_db'
--

--
-- Dumping routines for database 'five_star_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-03-21 15:07:42
