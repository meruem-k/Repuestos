-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: us-cdbr-east-06.cleardb.net    Database: heroku_323cf7babebbf2c
-- ------------------------------------------------------
-- Server version	5.6.50-log

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
-- Table structure for table `auto`
--

DROP TABLE IF EXISTS `auto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auto` (
  `MARCA` varchar(1000) NOT NULL,
  `MODELO` varchar(1000) NOT NULL,
  `ANIO` int(255) NOT NULL,
  `CODIGO_AUTO` int(255) NOT NULL,
  PRIMARY KEY (`CODIGO_AUTO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auto`
--

LOCK TABLES `auto` WRITE;
/*!40000 ALTER TABLE `auto` DISABLE KEYS */;
INSERT INTO `auto` VALUES ('Toyota','Yaris',2011,1);
INSERT INTO `auto` VALUES ('Chevrolet','Corsa',2008,2);
INSERT INTO `auto` VALUES ('Toyota','Yaris',2022,3);
INSERT INTO `auto` VALUES ('Toyota','RAV4',2022,4);
INSERT INTO `auto` VALUES ('Ford','Fiesta',2021,5);
INSERT INTO `auto` VALUES ('Toyota','RAV4',2011,6);
INSERT INTO `auto` VALUES ('Hyundai','Accent',2009,7);
INSERT INTO `auto` VALUES ('Mercedes Benz','A200',2017,8);
INSERT INTO `auto` VALUES ('Mercedes Benz','A200',2015,9);
INSERT INTO `auto` VALUES ('Mercedes Benz','A200',2022,10);
INSERT INTO `auto` VALUES ('Mercedes Benz','A200',2019,11);
INSERT INTO `auto` VALUES ('Toyota','A200',2022,12);
INSERT INTO `auto` VALUES ('Hyundai','Accent Hatchback',2018,13);
INSERT INTO `auto` VALUES ('Toyota','Yaris',2015,14);
INSERT INTO `auto` VALUES ('AA','Accent Hatchback',2018,15);
INSERT INTO `auto` VALUES ('Toyota','Yaris',2014,16);
INSERT INTO `auto` VALUES ('Hyundai','Sonata',1995,17);
INSERT INTO `auto` VALUES ('Ford','Taurus',2001,18);
/*!40000 ALTER TABLE `auto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registro_ventas`
--

DROP TABLE IF EXISTS `registro_ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registro_ventas` (
  `NOMBRE_REPUESTO` varchar(255) NOT NULL,
  `MARCA` varchar(255) NOT NULL,
  `MODELO` varchar(255) NOT NULL,
  `ANIO` int(255) NOT NULL,
  `UBICACION` varchar(255) NOT NULL,
  `PRECIO` int(11) NOT NULL,
  `CODIGO_BARRA` int(11) NOT NULL,
  `FECHA_VENTA` date NOT NULL,
  PRIMARY KEY (`CODIGO_BARRA`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registro_ventas`
--

LOCK TABLES `registro_ventas` WRITE;
/*!40000 ALTER TABLE `registro_ventas` DISABLE KEYS */;
INSERT INTO `registro_ventas` VALUES ('Freno','Hyundai','Sonata',1995,'BODEGA 1',50000,555555,'2022-10-05');
INSERT INTO `registro_ventas` VALUES ('Freno Trasero','Ford','Taurus',2001,'BODEGA 1',50000,3333333,'2022-10-05');
INSERT INTO `registro_ventas` VALUES ('Parachoque','AA','Accent Hatchback',2018,'HO67',78900,12345678,'2022-10-05');
INSERT INTO `registro_ventas` VALUES ('Neumatico','Kia','Rio 5',2021,'G8',10000,98766789,'2022-10-26');
/*!40000 ALTER TABLE `registro_ventas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repuesto`
--

DROP TABLE IF EXISTS `repuesto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repuesto` (
  `NOMBRE_REPUESTO` varchar(1000) NOT NULL,
  `UBICACION` varchar(1000) NOT NULL,
  `PRECIO` int(100) NOT NULL,
  `CODIGO_AUTO` int(255) NOT NULL,
  `CODIGO_BARRA` int(255) NOT NULL,
  `FOTO` varchar(5000) NOT NULL,
  PRIMARY KEY (`CODIGO_BARRA`),
  KEY `CODIGO_AUTO` (`CODIGO_AUTO`),
  CONSTRAINT `repuesto_ibfk_1` FOREIGN KEY (`CODIGO_AUTO`) REFERENCES `auto` (`CODIGO_AUTO`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repuesto`
--

LOCK TABLES `repuesto` WRITE;
/*!40000 ALTER TABLE `repuesto` DISABLE KEYS */;
INSERT INTO `repuesto` VALUES ('Freno','H1',21000,3,2147483647,'2022165659frenos_consejos.jpg');
/*!40000 ALTER TABLE `repuesto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resumen_ventas`
--

DROP TABLE IF EXISTS `resumen_ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resumen_ventas` (
  `NOMBRE_REPUESTO` varchar(255) NOT NULL,
  `MARCA` varchar(255) NOT NULL,
  `MODELO` varchar(255) NOT NULL,
  `ANIO` int(11) NOT NULL,
  `UBICACION` varchar(255) NOT NULL,
  `PRECIO` int(11) NOT NULL,
  `CODIGO_BARRA` int(11) NOT NULL,
  `FOTO` varchar(5000) DEFAULT NULL,
  `CODIGO_AUTO` int(11) DEFAULT NULL,
  PRIMARY KEY (`CODIGO_BARRA`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resumen_ventas`
--

LOCK TABLES `resumen_ventas` WRITE;
/*!40000 ALTER TABLE `resumen_ventas` DISABLE KEYS */;
/*!40000 ALTER TABLE `resumen_ventas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` smallint(3) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `password` varchar(5000) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=355 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (354,'DCARES','$2b$12$sD5Vpp8V4U9SsBIuijvsK.efzWZS88bkUS10TKrhZp2rjGyaIjG3.');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'heroku_323cf7babebbf2c'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-12-07 17:45:27
