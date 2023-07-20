-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: cronosdb
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `etiquetas`
--

DROP TABLE IF EXISTS `etiquetas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `etiquetas` (
  `idEtiqueta` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idEtiqueta`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `etiquetas`
--

LOCK TABLES `etiquetas` WRITE;
/*!40000 ALTER TABLE `etiquetas` DISABLE KEYS */;
INSERT INTO `etiquetas` VALUES (1,'cumpleaños'),(2,'torta'),(3,'comprar'),(4,'gordencia'),(65,'estudiar'),(66,'ingles'),(67,'programacion'),(68,'no procastines'),(69,'programacion 2');
/*!40000 ALTER TABLE `etiquetas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evento_etiqueta`
--

DROP TABLE IF EXISTS `evento_etiqueta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `evento_etiqueta` (
  `idEvento` int NOT NULL,
  `idEtiqueta` int NOT NULL,
  KEY `idEvento` (`idEvento`),
  KEY `idEtiqueta` (`idEtiqueta`),
  CONSTRAINT `evento_etiqueta_ibfk_1` FOREIGN KEY (`idEvento`) REFERENCES `eventos` (`idEvento`),
  CONSTRAINT `evento_etiqueta_ibfk_2` FOREIGN KEY (`idEtiqueta`) REFERENCES `etiquetas` (`idEtiqueta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evento_etiqueta`
--

LOCK TABLES `evento_etiqueta` WRITE;
/*!40000 ALTER TABLE `evento_etiqueta` DISABLE KEYS */;
INSERT INTO `evento_etiqueta` VALUES (1,1),(1,2),(1,3),(1,4),(49,65),(49,66),(50,68),(50,69);
/*!40000 ALTER TABLE `evento_etiqueta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventos`
--

DROP TABLE IF EXISTS `eventos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventos` (
  `idEvento` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(30) NOT NULL,
  `duracion` int DEFAULT NULL,
  `fecha_y_hora_e` datetime DEFAULT NULL,
  `fecha_y_hora_r` datetime DEFAULT NULL,
  `detalle` varchar(100) DEFAULT NULL,
  `import` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`idEvento`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventos`
--

LOCK TABLES `eventos` WRITE;
/*!40000 ALTER TABLE `eventos` DISABLE KEYS */;
INSERT INTO `eventos` VALUES (1,'cumpleaños de can can',60,'2023-07-06 12:00:00','2023-07-06 00:00:00','cumpleaños de la gordencia, comprar torta',1),(49,'estudiar ingles',120,'2023-07-17 14:32:34','2023-07-01 00:00:00','DEBES ESTUDIAR SI O SI',1),(50,'estudiar programacion2',200,'2023-07-17 16:38:09','2023-07-02 00:00:00','DEBES ESTUDIAR',1);
/*!40000 ALTER TABLE `eventos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-20  0:57:35
