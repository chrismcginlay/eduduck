-- MySQL dump 10.13  Distrib 5.5.31, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: eduduck
-- ------------------------------------------------------
-- Server version	5.5.31-0ubuntu0.12.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `attachment_attachment`
--

DROP TABLE IF EXISTS `attachment_attachment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `attachment_attachment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `att_code` varchar(10) DEFAULT NULL,
  `att_name` varchar(200) NOT NULL,
  `lesson_id` int(11) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  `att_desc` longtext,
  `att_seq` int(11) DEFAULT NULL,
  `attachment` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lesson_id` (`lesson_id`,`att_seq`),
  UNIQUE KEY `course_id` (`course_id`,`att_seq`),
  CONSTRAINT `course_id_refs_id_6ddd5347` FOREIGN KEY (`course_id`) REFERENCES `courses_course` (`id`),
  CONSTRAINT `lesson_id_refs_id_2ae5454a` FOREIGN KEY (`lesson_id`) REFERENCES `courses_lesson` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attachment_attachment`
--

LOCK TABLES `attachment_attachment` WRITE;
/*!40000 ALTER TABLE `attachment_attachment` DISABLE KEYS */;
INSERT INTO `attachment_attachment` VALUES (1,'BLL1','FaceViewCube',3,NULL,'',1,'attachments/faceviewcube_1.blend'),(2,'BLL2','CubeStack starting file',6,NULL,'Starting file for cube stacking exercise',3,'attachments/cube_stack1_1.blend'),(3,'BLL3','CubeStack keyframe animation',6,NULL,'Working animated cube stack using keyframes',4,'attachments/cube_stack2.blend'),(4,'BLL4','The Basic User Interface',2,NULL,'Graphic showing the names of the 5 main parts of the default user interface.',NULL,'attachments/blender_ui_annotated_1.png');
/*!40000 ALTER TABLE `attachment_attachment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `permission_id_refs_id_5886d21f` (`permission_id`),
  CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_5886d21f` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add site',6,'add_site'),(17,'Can change site',6,'change_site'),(18,'Can delete site',6,'delete_site'),(19,'Can add log entry',7,'add_logentry'),(20,'Can change log entry',7,'change_logentry'),(21,'Can delete log entry',7,'delete_logentry'),(22,'Can add course',8,'add_course'),(23,'Can change course',8,'change_course'),(24,'Can delete course',8,'delete_course'),(25,'Can add lesson',9,'add_lesson'),(26,'Can change lesson',9,'change_lesson'),(27,'Can delete lesson',9,'delete_lesson'),(28,'Can add video',10,'add_video'),(29,'Can change video',10,'change_video'),(30,'Can delete video',10,'delete_video'),(31,'Can add answer',11,'add_answer'),(32,'Can change answer',11,'change_answer'),(33,'Can delete answer',11,'delete_answer'),(34,'Can add question',12,'add_question'),(35,'Can change question',12,'change_question'),(36,'Can delete question',12,'delete_question'),(37,'Can add quiz',13,'add_quiz'),(38,'Can change quiz',13,'change_quiz'),(39,'Can delete quiz',13,'delete_quiz'),(40,'Can add quiz attempt',14,'add_quizattempt'),(41,'Can change quiz attempt',14,'change_quizattempt'),(42,'Can delete quiz attempt',14,'delete_quizattempt'),(43,'Can add question attempt',15,'add_questionattempt'),(44,'Can change question attempt',15,'change_questionattempt'),(45,'Can delete question attempt',15,'delete_questionattempt'),(46,'Can add bio',16,'add_bio'),(47,'Can change bio',16,'change_bio'),(48,'Can delete bio',16,'delete_bio'),(49,'Can add user course',17,'add_usercourse'),(50,'Can change user course',17,'change_usercourse'),(51,'Can delete user course',17,'delete_usercourse'),(52,'Can add user lesson',18,'add_userlesson'),(53,'Can change user lesson',18,'change_userlesson'),(54,'Can delete user lesson',18,'delete_userlesson'),(55,'Can add user learning intention',19,'add_userlearningintention'),(56,'Can change user learning intention',19,'change_userlearningintention'),(57,'Can delete user learning intention',19,'delete_userlearningintention'),(58,'Can add user\'s learning intention detail',20,'add_userlearningintentiondetail'),(59,'Can change user\'s learning intention detail',20,'change_userlearningintentiondetail'),(60,'Can delete user\'s learning intention detail',20,'delete_userlearningintentiondetail'),(61,'Can add user attachment',21,'add_userattachment'),(62,'Can change user attachment',21,'change_userattachment'),(63,'Can delete user attachment',21,'delete_userattachment'),(64,'Can add learning intention',22,'add_learningintention'),(65,'Can change learning intention',22,'change_learningintention'),(66,'Can delete learning intention',22,'delete_learningintention'),(67,'Can add learning intention detail',23,'add_learningintentiondetail'),(68,'Can change learning intention detail',23,'change_learningintentiondetail'),(69,'Can delete learning intention detail',23,'delete_learningintentiondetail'),(70,'Can add attachment',24,'add_attachment'),(71,'Can change attachment',24,'change_attachment'),(72,'Can delete attachment',24,'delete_attachment'),(73,'Can add registration profile',25,'add_registrationprofile'),(74,'Can change registration profile',25,'change_registrationprofile'),(75,'Can delete registration profile',25,'delete_registrationprofile');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'gaffer','','','chris@unpossible.info','pbkdf2_sha256$10000$R5hwRcXGWr6W$Aed9XejR18ICr9aT3G155kcLYpceEqo2Rfo2Qla6Qv4=',1,1,1,'2013-06-30 14:16:53','2013-06-23 00:02:57'),(15,'alanm','','','alanm@sics.se','pbkdf2_sha256$10000$cx4VtvPz96xa$z+U8Bzr8B7FWY+peEalvQgsMv8J8kM5f+xGlbTY6yV4=',0,1,0,'2013-06-25 21:22:07','2013-06-25 21:22:07'),(17,'chrismcginlay','','','ctmcginlay@gmail.com','pbkdf2_sha256$10000$7jp6ICoIHMoI$4fbaB78GM7I1XG3tu+yjBvXC3zIuL33ZzeNNB7HfY8s=',0,0,0,'2013-06-26 22:53:53','2013-06-26 22:53:53'),(18,'chris','','','ctmcginlay@gmail.com','pbkdf2_sha256$10000$UPMdKt5in0Xo$lswjJp4uJZxrPBCs0HVTdxbYBSdNoRrvzcc0tQeP4tY=',0,0,0,'2013-06-27 20:39:00','2013-06-27 20:39:00'),(19,'duncannonuts','','','chris@ascentsoftware.org.uk','pbkdf2_sha256$10000$3ZrMC4yngZbI$U9BDmTdmnNg/jVCKDrXUbpBuInuLLsaGNzkZ2iOqJXk=',0,0,0,'2013-06-27 20:44:06','2013-06-27 20:44:06'),(20,'alanm2','','','alanm@sics.se','pbkdf2_sha256$10000$bpCm59e1gT3e$y/dE7OJTXX6r+wAHxsYBMdjM5HwxG/AmeRmASx6V2T4=',0,1,0,'2013-06-30 19:58:01','2013-06-28 09:39:30'),(21,'testtestersson','','','alanm@sics.se','pbkdf2_sha256$10000$fHhxjtuKbxlX$8MCzqs48jsVjoxyhaZUFt86PNEdWVn5iKcmJ3qDpk0I=',0,0,0,'2013-06-28 09:41:35','2013-06-28 09:41:35'),(22,'alanm3','','','mrintegrity@gmail.com','pbkdf2_sha256$10000$FYvM7Xfl15nH$KIuQEdvcpptPuWVZyJgffVnZQ0YOwyuhW1NdJ3pzmvs=',0,1,0,'2013-06-28 09:42:51','2013-06-28 09:42:51'),(23,'alanm4','','','mcginlay.alan@gmail.com','pbkdf2_sha256$10000$HfxRaugs7BFQ$n2OmwNyWWA1nCiH03VFNNiblymrfIZSO8ESOKSLnh6Y=',0,1,0,'2013-06-28 09:46:42','2013-06-28 09:45:11');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `group_id_refs_id_f116770` (`group_id`),
  CONSTRAINT `group_id_refs_id_f116770` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_7ceef80f` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `permission_id_refs_id_67e79cb` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_dfbab7d` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bio_bio`
--

DROP TABLE IF EXISTS `bio_bio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bio_bio` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `user_tz` varchar(255) NOT NULL,
  `accepted_terms` tinyint(1) NOT NULL,
  `signature_line` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `webpage` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_11eec5ba` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bio_bio`
--

LOCK TABLES `bio_bio` WRITE;
/*!40000 ALTER TABLE `bio_bio` DISABLE KEYS */;
INSERT INTO `bio_bio` VALUES (1,1,'Atlantic/St_Helena',1,'Administration account','',''),(3,17,'',0,'','',''),(4,18,'',0,'','',''),(5,19,'',0,'','',''),(6,20,'',0,'','',''),(7,21,'',0,'','',''),(8,22,'',0,'','',''),(9,23,'',0,'','','');
/*!40000 ALTER TABLE `bio_bio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses_course`
--

DROP TABLE IF EXISTS `courses_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courses_course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_code` varchar(10) NOT NULL,
  `course_name` varchar(150) NOT NULL,
  `course_abstract` longtext NOT NULL,
  `course_organiser` varchar(100) NOT NULL,
  `course_level` varchar(10) DEFAULT NULL,
  `course_credits` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses_course`
--

LOCK TABLES `courses_course` WRITE;
/*!40000 ALTER TABLE `courses_course` DISABLE KEYS */;
INSERT INTO `courses_course` VALUES (1,'ARTBL1','Up and Running with Blender','Blender is powerful 3D modelling and animation software. You can use it to create industrial class animations, or high quality still images in photo-realistic, cartoon or blueprint styles. Blender offers a relatively complete animation workflow, or you can use it alongside other tools such as OpenShot, Final Cut Pro etc.\r\n\r\n3D modelling and animation has a reputation for being hard. This beginners\' course aims to get you quickly over the initial learning curve. \r\n\r\nThis is a tried and tested course, clear and well structured in its goals. Most of the lessons focus on a single aspect of modelling or animating and come with partially constructed example files to support your learning.\r\n\r\nThe approach taken here is different from most online tutorials. There are a large selection of these online, uploaded by many great Blender enthusiasts. Many of these take you through a complex series of steps, covering dozens of concepts with the objective of producing a finished product. That style of presentation can lead to frustration and confusion, particulary when starting out. That said, there are many, many truly excellent and enjoyable tutorials out there, produced by very competent and helpful people. Towards the end of the course, links to other learning resources are included.\r\n','Chris McGinlay','Beginner',10);
/*!40000 ALTER TABLE `courses_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses_lesson`
--

DROP TABLE IF EXISTS `courses_lesson`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courses_lesson` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lesson_code` varchar(10) DEFAULT NULL,
  `lesson_name` varchar(200) NOT NULL,
  `course_id` int(11) NOT NULL,
  `abstract` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_id_refs_id_43f0cbf4` (`course_id`),
  CONSTRAINT `course_id_refs_id_43f0cbf4` FOREIGN KEY (`course_id`) REFERENCES `courses_course` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses_lesson`
--

LOCK TABLES `courses_lesson` WRITE;
/*!40000 ALTER TABLE `courses_lesson` DISABLE KEYS */;
INSERT INTO `courses_lesson` VALUES (1,'BL1','What is Blender?',1,'Be clear what Blender is, where to download it, what it can achieve and where to find sources of community support.'),(2,'BL2','The User Interface',1,'Here we outline the purpose of the main areas of Blender\'s screen or user interface.'),(3,'BL3','Controlling the View',1,'Learn how to use the number pad to control your viewing direction in the 3D viewport.'),(4,'BL4','Basic Object Selection',1,'Practise using the object outliner and mouse/keyboard to select objects, see how the Object Properties and Buttons Window changes depending on selection, change lamp color and produce a quick render.'),(5,'BL5','Controlling Object Position',1,'Use transform manipulators and GRS hotkeys to control object position.\r\nUse axis constraints, and see how to do transforms over discrete and continuous distances.\r\nDirectly setting location, rotation and scale in the Object Properties area.'),(6,'BL6','Quick Keyframe Animation',1,'Show just how easy it is to produce a basic animation.\r\nUnderstand how to insert keyframes and review work in the timeline area.\r\nUnderstand the significance of framerate.');
/*!40000 ALTER TABLE `courses_lesson` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses_video`
--

DROP TABLE IF EXISTS `courses_video`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courses_video` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `video_code` varchar(10) DEFAULT NULL,
  `video_name` varchar(200) NOT NULL,
  `url` varchar(200) NOT NULL,
  `lesson_id` int(11) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `lesson_id_refs_id_42060511` (`lesson_id`),
  KEY `course_id_refs_id_2b62f420` (`course_id`),
  CONSTRAINT `course_id_refs_id_2b62f420` FOREIGN KEY (`course_id`) REFERENCES `courses_course` (`id`),
  CONSTRAINT `lesson_id_refs_id_42060511` FOREIGN KEY (`lesson_id`) REFERENCES `courses_lesson` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses_video`
--

LOCK TABLES `courses_video` WRITE;
/*!40000 ALTER TABLE `courses_video` DISABLE KEYS */;
INSERT INTO `courses_video` VALUES (2,'BL1','Lesson 1: What is Blender?','http://youtube.com/embed/b5qZnK_7f6U?rel=0',1,NULL),(3,'BL2','Lesson 2: The User Interface','http://www.youtube.com/embed/8sJi9-1Hq_c?rel=0',2,NULL),(4,'BL3a','Lesson 3a: Controlling the View','http://youtube.com/embed/2_lCLMYuOZI?rel=0',3,NULL),(5,'BL3b','Lesson 3b: 3D Cartesian Co-ordinates','http://youtube.com/embed/00wabfcXKE0?rel=0',3,NULL),(6,'BL4','Lesson 4: Basic Object Selection','http://youtube.com/embed/t0Y3hanK8JY?rel=0',4,NULL),(7,'BL5','Lesson 5: Controlling Object Position','http://youtube.com/embed/gaN8ktFPvys?rel=0',5,NULL),(8,'BL6','Lesson 6: A Quick Keyframe Animation','http://youtube.com/embed/T4W1LyweDBs?rel=0',6,NULL),(9,'BL6b','Lesson 6b: Keyframe Cube Stacking Exercise','http://youtube.com/embed/wK-HrdmCBas?rel=0',6,NULL),(10,'BL6c','Lesson 6: A Quick Keyframe Animation - Solution','http://youtube.com/embed/girYNzSgh_o?rel=0',6,NULL);
/*!40000 ALTER TABLE `courses_video` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id_refs_id_c8665aa` (`user_id`),
  KEY `content_type_id_refs_id_288599e6` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_288599e6` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c8665aa` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2013-06-23 21:05:58',1,6,'1','eduduck.com',2,'Changed domain and name.'),(2,'2013-06-30 16:07:08',1,8,'1','Up and Running with Blender',1,''),(3,'2013-06-30 16:12:29',1,8,'1','Up and Running with Blender',2,'Changed course_abstract.'),(4,'2013-06-30 16:44:52',1,9,'1','What is Blender?',1,''),(5,'2013-06-30 16:48:18',1,10,'1','Lesson 1: What is Blender?',1,''),(6,'2013-06-30 17:48:28',1,10,'2','Lesson 1: What is Blender?',1,''),(7,'2013-07-03 13:33:51',1,22,'1','Appreciate the range of tasks that you can use Blender for',1,''),(8,'2013-07-03 13:35:06',1,22,'2','Know where to get a copy of Blender',1,''),(9,'2013-07-03 13:36:08',1,22,'3','Know about a selection of community support websites',1,''),(10,'2013-07-03 16:08:33',1,22,'2','Find out where to get a copy of Blender',2,'Changed li_text.'),(11,'2013-07-03 16:09:24',1,22,'3','See what sort of help is available from some community support websites',2,'Changed li_text.'),(12,'2013-07-03 16:10:10',1,22,'1','Explore the range of tasks that you can use Blender for',2,'Changed li_text.'),(13,'2013-07-03 16:12:40',1,22,'3','See what sort of help is available from some community support websites',2,'Changed lid_text for learning intention detail \"Find my way around some of the Blender forums and community websites\".'),(14,'2013-07-03 16:13:24',1,22,'2','Find out where to get a copy of Blender',2,'Changed lid_text for learning intention detail \"Download and install the correct version of Blender for my computer.\".'),(15,'2013-07-03 16:14:01',1,22,'1','Explore the range of tasks that you can use Blender for',2,'Changed lid_text for learning intention detail \"Give examples of tasks which Blender is designed to do\".'),(16,'2013-07-03 16:18:19',1,9,'1','What is Blender?',2,'No fields changed.'),(17,'2013-07-03 16:21:03',1,9,'2','The User Interface',1,''),(18,'2013-07-03 16:49:33',1,22,'4','Become familiar with the main parts of the default user interface',1,''),(19,'2013-07-03 17:03:03',1,22,'4','Become familiar with the main parts of the default user interface',2,'Changed lid_text for learning intention detail \"Toggle the object properties panel by pressing N, or using the menu\".'),(20,'2013-07-04 09:10:56',1,10,'2','Lesson 1: What is Blender?',2,'Changed url.'),(21,'2013-07-05 00:04:24',1,10,'3','Lesson 2: The User Interface',1,''),(22,'2013-07-05 23:03:16',1,9,'3','Controlliing the View',1,''),(23,'2013-07-05 23:03:47',1,9,'3','Controlling the View',2,'Changed lesson_name.'),(24,'2013-07-05 23:04:52',1,9,'3','Controlling the View',2,'Changed abstract.'),(25,'2013-07-07 17:29:21',1,10,'4','Lesson 3: Controlling the View',1,''),(26,'2013-07-07 21:50:46',1,22,'1','Explore the range of tasks that you can use Blender for',2,'Added learning intention detail \"State suitable tasks which can be achieved with Blender\".'),(27,'2013-07-07 21:53:09',1,22,'2','Find out where to get a copy of Blender',2,'Added learning intention detail \"State that www.blender.org has downloadable install files for Blender\".'),(28,'2013-07-07 21:54:04',1,22,'3','See what sort of help is available from some community support websites',2,'Added learning intention detail \"Give 2 examples of Blender discussion forums\".'),(29,'2013-07-07 22:02:11',1,22,'5','See how to use the number pad to control your viewing direction in the 3D viewport',1,''),(30,'2013-07-07 22:05:09',1,22,'5','See how to use the number pad to control your viewing direction in the 3D viewport',2,'Added learning intention detail \"Identify the axes indicator in the 3D viewport\".'),(31,'2013-07-07 22:10:29',1,22,'6','Understand the basic idea of 3D Cartesian co-ordinates',1,''),(32,'2013-07-07 22:12:11',1,22,'6','Understand the basic idea of 3D Cartesian co-ordinates',2,'Added learning intention detail \"State that Blender embeds colour coded axes into the grid floor\". Changed lid_text for learning intention detail \"State that Blender colour codes (x,y,z) axes as (Red, Green, Blue) respectively\".'),(33,'2013-07-07 22:13:07',1,22,'6','Understand the basic idea of 3D Cartesian co-ordinates',2,'Changed lid_text for learning intention detail \"Use your right hand to understand the relation between the x,y, and z axes in 3D Cartesian co-ordinates\".'),(34,'2013-07-08 00:09:41',1,10,'5','3D Cartesian Co-ordinates',1,''),(35,'2013-07-08 00:13:14',1,10,'5','Lesson 3b: 3D Cartesian Co-ordinates',2,'Changed video_name.'),(36,'2013-07-08 00:13:46',1,10,'4','Lesson 3a: Controlling the View',2,'Changed video_name.'),(37,'2013-07-08 11:24:30',1,9,'4','Basic Object Selection',1,''),(38,'2013-07-08 11:37:08',1,22,'7','Practise using the object outliner and mouse/keyboard to select objects.',1,''),(39,'2013-07-08 11:40:49',1,22,'8','See how the Object Properties and Buttons Window changes depending on selection',1,''),(40,'2013-07-08 11:41:21',1,22,'7','Practise using the object outliner and mouse/keyboard to select objects.',2,'Deleted learning intention detail \"Know how to change the name of an object\". Deleted learning intention detail \"Use sensible names for the objects in your own Blender projects\". Deleted learning intention detail \"Know that each object\'s object data can be viewed and editied directly\". Deleted learning intention detail \"Experiment with some basic object data changes and produce a selection of renders\".'),(41,'2013-07-08 11:42:34',1,22,'7','Practise using the object outliner and mouse/keyboard to select objects.',2,'Deleted learning intention detail \"Give two methods of producing a render (keyboard and mouse)\".'),(42,'2013-07-08 11:42:44',1,22,'9','Change lamp colour and produce a quick render',1,''),(43,'2013-07-08 11:43:57',1,22,'8','See how the Object Properties and Buttons Window changes depending on selection',2,'Changed lid_text for learning intention detail \"Know that each object\'s object data can be viewed and edited directly\".'),(44,'2013-07-08 13:33:34',1,24,'1','Att. ID:1, code:BLL1, \'FaceViewCu...\'',1,''),(45,'2013-07-08 13:51:05',1,9,'5','Controlling Object Position',1,''),(46,'2013-07-08 13:51:59',1,9,'6','Quick Keyframe Animation',1,''),(47,'2013-07-08 13:55:29',1,24,'2','Att. ID:2, code:BLL2, \'CubeStack ...\'',1,''),(48,'2013-07-08 13:56:59',1,24,'3','Att. ID:3, code:BLL3, \'CubeStack ...\'',1,''),(49,'2013-07-08 22:28:59',1,10,'6','Lesson 4: Basic Object Selection',1,''),(50,'2013-07-08 23:57:16',1,10,'7','Lesson 5: Controlling Object Position',1,''),(51,'2013-07-09 00:24:38',1,10,'8','A Quick Keyframe Animation',1,''),(52,'2013-07-09 00:25:12',1,10,'8','Lesson 6: A Quick Keyframe Animation',2,'Changed video_name.'),(53,'2013-07-09 09:23:57',1,24,'2','Att. ID:2, code:BLL2, \'CubeStack ...\'',2,'Changed attachment.'),(54,'2013-07-09 22:26:55',1,10,'9','Lesson 6: Keyframe Cube Stacking Exercise',1,''),(55,'2013-07-09 22:27:18',1,10,'9','Lesson 6b: Keyframe Cube Stacking Exercise',2,'Changed video_name.'),(56,'2013-07-09 22:27:39',1,10,'8','Lesson 6: A Quick Keyframe Animation',2,'Changed course.'),(57,'2013-07-09 22:27:47',1,10,'7','Lesson 5: Controlling Object Position',2,'Changed course.'),(58,'2013-07-09 22:28:02',1,10,'6','Lesson 4: Basic Object Selection',2,'Changed course.'),(59,'2013-07-09 22:28:11',1,10,'5','Lesson 3b: 3D Cartesian Co-ordinates',2,'Changed course.'),(60,'2013-07-09 22:28:24',1,10,'3','Lesson 2: The User Interface',2,'Changed course.'),(61,'2013-07-09 22:28:32',1,10,'2','Lesson 1: What is Blender?',2,'Changed course.'),(62,'2013-07-09 22:29:01',1,10,'4','Lesson 3a: Controlling the View',2,'Changed course.'),(63,'2013-07-09 22:29:24',1,24,'3','Att. ID:3, code:BLL3, \'CubeStack ...\'',2,'Changed course.'),(64,'2013-07-09 22:29:34',1,24,'2','Att. ID:2, code:BLL2, \'CubeStack ...\'',2,'Changed course.'),(65,'2013-07-09 22:29:53',1,24,'1','Att. ID:1, code:BLL1, \'FaceViewCu...\'',2,'Changed course.'),(66,'2013-07-10 00:04:41',1,22,'10','Perform Transformations on Objects',1,''),(67,'2013-07-10 00:15:19',1,22,'11','Apply constraints to the object transforms',1,''),(68,'2013-07-10 00:18:59',1,22,'12','Directly inspect or change transform properties in the object properties area',1,''),(69,'2013-07-10 09:34:01',1,10,'10','Lesson 6: A Quick Keyframe Animation - Solution',1,''),(70,'2013-07-11 22:10:09',1,22,'13','Create a simple animation using keyframes',1,''),(71,'2013-07-11 22:14:50',1,22,'14','Use a simple procedure to insert keyframes',1,''),(72,'2013-07-11 22:18:28',1,22,'15','Review animation work using the timeline',1,''),(73,'2013-07-11 22:27:37',1,24,'4','Att. ID:4, code:BLL4, \'The Basic ...\'',1,'');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'site','sites','site'),(7,'log entry','admin','logentry'),(8,'course','courses','course'),(9,'lesson','courses','lesson'),(10,'video','courses','video'),(11,'answer','quiz','answer'),(12,'question','quiz','question'),(13,'quiz','quiz','quiz'),(14,'quiz attempt','quiz','quizattempt'),(15,'question attempt','quiz','questionattempt'),(16,'bio','bio','bio'),(17,'user course','interaction','usercourse'),(18,'user lesson','interaction','userlesson'),(19,'user learning intention','interaction','userlearningintention'),(20,'user\'s learning intention detail','interaction','userlearningintentiondetail'),(21,'user attachment','interaction','userattachment'),(22,'learning intention','outcome','learningintention'),(23,'learning intention detail','outcome','learningintentiondetail'),(24,'attachment','attachment','attachment'),(25,'registration profile','registration','registrationprofile');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('18732fd472484ba34df8a84d21bdac32','OWI4ZTA0MmJkMTBjMmNjYTUwM2RhM2Q5OTg3OWUxN2NiMzZjZDVjMjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2013-07-14 14:16:53'),('7b3c6ed11ff871a002c29b24b370ad45','Y2U1MjQ5YzI1MzJjMGI2MjEyOTVjZjM3NDQzZWI3MjUyY2NkMDQ0MjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKARR1Lg==\n','2013-07-14 19:58:01');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'eduduck.com','EduDuck');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interaction_userattachment`
--

DROP TABLE IF EXISTS `interaction_userattachment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interaction_userattachment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `attachment_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `history` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `attachment_id` (`attachment_id`,`user_id`),
  KEY `user_id_refs_id_5d00ad17` (`user_id`),
  CONSTRAINT `attachment_id_refs_id_432a2188` FOREIGN KEY (`attachment_id`) REFERENCES `attachment_attachment` (`id`),
  CONSTRAINT `user_id_refs_id_5d00ad17` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interaction_userattachment`
--

LOCK TABLES `interaction_userattachment` WRITE;
/*!40000 ALTER TABLE `interaction_userattachment` DISABLE KEYS */;
/*!40000 ALTER TABLE `interaction_userattachment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interaction_usercourse`
--

DROP TABLE IF EXISTS `interaction_usercourse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interaction_usercourse` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `withdrawn` tinyint(1) NOT NULL,
  `completed` tinyint(1) NOT NULL,
  `history` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `course_id` (`course_id`,`user_id`),
  KEY `user_id_refs_id_2bda4a93` (`user_id`),
  CONSTRAINT `course_id_refs_id_2b4fc290` FOREIGN KEY (`course_id`) REFERENCES `courses_course` (`id`),
  CONSTRAINT `user_id_refs_id_2bda4a93` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interaction_usercourse`
--

LOCK TABLES `interaction_usercourse` WRITE;
/*!40000 ALTER TABLE `interaction_usercourse` DISABLE KEYS */;
/*!40000 ALTER TABLE `interaction_usercourse` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interaction_userlearningintention`
--

DROP TABLE IF EXISTS `interaction_userlearningintention`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interaction_userlearningintention` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `learning_intention_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`learning_intention_id`),
  KEY `learning_intention_id_refs_id_4f552ef8` (`learning_intention_id`),
  CONSTRAINT `learning_intention_id_refs_id_4f552ef8` FOREIGN KEY (`learning_intention_id`) REFERENCES `outcome_learningintention` (`id`),
  CONSTRAINT `user_id_refs_id_14e0224f` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interaction_userlearningintention`
--

LOCK TABLES `interaction_userlearningintention` WRITE;
/*!40000 ALTER TABLE `interaction_userlearningintention` DISABLE KEYS */;
INSERT INTO `interaction_userlearningintention` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,1,5),(6,1,6),(7,1,7),(8,1,8),(9,1,9),(10,1,10),(11,1,11),(12,1,12),(13,1,13),(14,1,14),(15,1,15);
/*!40000 ALTER TABLE `interaction_userlearningintention` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interaction_userlearningintentiondetail`
--

DROP TABLE IF EXISTS `interaction_userlearningintentiondetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interaction_userlearningintentiondetail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `learning_intention_detail_id` int(11) NOT NULL,
  `condition` smallint(6) NOT NULL,
  `history` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`learning_intention_detail_id`),
  KEY `learning_intention_detail_id_refs_id_353d63aa` (`learning_intention_detail_id`),
  CONSTRAINT `learning_intention_detail_id_refs_id_353d63aa` FOREIGN KEY (`learning_intention_detail_id`) REFERENCES `outcome_learningintentiondetail` (`id`),
  CONSTRAINT `user_id_refs_id_475f9f0` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interaction_userlearningintentiondetail`
--

LOCK TABLES `interaction_userlearningintentiondetail` WRITE;
/*!40000 ALTER TABLE `interaction_userlearningintentiondetail` DISABLE KEYS */;
INSERT INTO `interaction_userlearningintentiondetail` VALUES (1,1,5,0,NULL);
/*!40000 ALTER TABLE `interaction_userlearningintentiondetail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interaction_userlesson`
--

DROP TABLE IF EXISTS `interaction_userlesson`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interaction_userlesson` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lesson_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `visited` tinyint(1) NOT NULL,
  `completed` tinyint(1) NOT NULL,
  `history` longtext,
  `note` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lesson_id` (`lesson_id`,`user_id`),
  KEY `user_id_refs_id_5ed3507c` (`user_id`),
  CONSTRAINT `lesson_id_refs_id_3ff8be96` FOREIGN KEY (`lesson_id`) REFERENCES `courses_lesson` (`id`),
  CONSTRAINT `user_id_refs_id_5ed3507c` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interaction_userlesson`
--

LOCK TABLES `interaction_userlesson` WRITE;
/*!40000 ALTER TABLE `interaction_userlesson` DISABLE KEYS */;
/*!40000 ALTER TABLE `interaction_userlesson` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `outcome_learningintention`
--

DROP TABLE IF EXISTS `outcome_learningintention`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `outcome_learningintention` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lesson_id` int(11) NOT NULL,
  `li_text` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lesson_id_refs_id_462fce74` (`lesson_id`),
  CONSTRAINT `lesson_id_refs_id_462fce74` FOREIGN KEY (`lesson_id`) REFERENCES `courses_lesson` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `outcome_learningintention`
--

LOCK TABLES `outcome_learningintention` WRITE;
/*!40000 ALTER TABLE `outcome_learningintention` DISABLE KEYS */;
INSERT INTO `outcome_learningintention` VALUES (1,1,'Explore the range of tasks that you can use Blender for'),(2,1,'Find out where to get a copy of Blender'),(3,1,'See what sort of help is available from some community support websites'),(4,2,'Become familiar with the main parts of the default user interface'),(5,3,'See how to use the number pad to control your viewing direction in the 3D viewport'),(6,3,'Understand the basic idea of 3D Cartesian co-ordinates'),(7,4,'Practise using the object outliner and mouse/keyboard to select objects.'),(8,4,'See how the Object Properties and Buttons Window changes depending on selection'),(9,4,'Change lamp colour and produce a quick render'),(10,5,'Perform Transformations on Objects'),(11,5,'Apply constraints to the object transforms'),(12,5,'Directly inspect or change transform properties in the object properties area'),(13,6,'Create a simple animation using keyframes'),(14,6,'Use a simple procedure to insert keyframes'),(15,6,'Review animation work using the timeline');
/*!40000 ALTER TABLE `outcome_learningintention` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `outcome_learningintentiondetail`
--

DROP TABLE IF EXISTS `outcome_learningintentiondetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `outcome_learningintentiondetail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `learning_intention_id` int(11) NOT NULL,
  `lid_text` varchar(200) NOT NULL,
  `lid_type` varchar(2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `learning_intention_id_refs_id_20042d2` (`learning_intention_id`),
  CONSTRAINT `learning_intention_id_refs_id_20042d2` FOREIGN KEY (`learning_intention_id`) REFERENCES `outcome_learningintention` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `outcome_learningintentiondetail`
--

LOCK TABLES `outcome_learningintentiondetail` WRITE;
/*!40000 ALTER TABLE `outcome_learningintentiondetail` DISABLE KEYS */;
INSERT INTO `outcome_learningintentiondetail` VALUES (1,1,'Give examples of tasks which Blender is designed to do','SC'),(2,2,'Download and install the correct version of Blender for my computer.','SC'),(3,3,'Find my way around some of the Blender forums and community websites','SC'),(4,4,'Identify the 3D viewport','LO'),(5,4,'Differentiate between the 3D cursor, object manipulator, and object centre.','LO'),(6,4,'Identify the xyz axis graphic','LO'),(7,4,'Identify the timeline','LO'),(8,4,'Identify the toolshelf','LO'),(9,4,'Identify the object properties panel','LO'),(10,4,'Identify the buttons window','LO'),(11,4,'Move the 3D cursor using mouse-clicks','SC'),(12,4,'Add new objects at the cursor position','SC'),(13,4,'Change the object manipulator style, or turn it off completely','SC'),(14,4,'Toggle the toolshelf visibility by pressing T, or using the menu','SC'),(15,4,'Toggle the object properties panel by pressing N, or using the menu','SC'),(16,4,'Directly alter the location and rotation data for the default cube in the object properties panel','SC'),(17,1,'State suitable tasks which can be achieved with Blender','LO'),(18,2,'State that www.blender.org has downloadable install files for Blender','LO'),(19,3,'Give 2 examples of Blender discussion forums','LO'),(20,5,'Readily switch between 6 main views directed along co-ordinate axes','SC'),(21,5,'Toggle orthoscopic and perspective views','SC'),(22,5,'Switch to camera view to see how the scene will render','SC'),(23,5,'Use the axes indicator in the 3D viewport to help with orientiation','SC'),(24,5,'Explore all the different view options in the view menu and see the corresponding keyboard shortcut','SC'),(25,5,'State the keyboard shortcuts for front, right-side and top views','LO'),(26,5,'State the keyboard shortcuts for back, left and bottom views.','LO'),(27,5,'State the effect of 5, /, 0, Home number pad keys on the 3D viewport','LO'),(28,5,'State how to rotate the view in 15 degree steps','LO'),(29,5,'Know how to use the view menu to find keyboard shortcuts','LO'),(30,5,'Identify the axes indicator in the 3D viewport','LO'),(31,6,'Understand how to extend (x,y) co-ordinates in a plane into (x,y,z) co-ordinates in 3D space','LO'),(32,6,'State that Blender colour codes (x,y,z) axes as (Red, Green, Blue) respectively','LO'),(33,6,'Use the 3D axis indicator to help orient yourself when rotating the view','SC'),(34,6,'Be able to use (and control) the co-ordinate axes embedded in the grid floor','SC'),(35,6,'Use your right hand to understand the relation between the x,y, and z axes in 3D Cartesian co-ordinates','SC'),(36,6,'State that Blender embeds colour coded axes into the grid floor','LO'),(37,7,'Identify the object outliner','LO'),(38,7,'Use the object outliner to select individual objects in a scene','SC'),(41,7,'Select objects in a scene by right clicking','SC'),(45,8,'Know how to change the name of an object','LO'),(46,8,'Use sensible names for the objects in your own Blender projects','SC'),(47,8,'Know that each object\'s object data can be viewed and edited directly','LO'),(48,8,'Experiment with some basic object data changes and produce a selection of render','SC'),(49,9,'Give two methods of producing a render (keyboard and mouse)','LO'),(50,9,'Experiment with some basic object properties such as lamp colour','SC'),(51,10,'State the 3 basic object transforms','LO'),(52,10,'Use the correct keyboard shortcut for Grab, Rotate, and Scale transforms','SC'),(53,10,'State two methods for accepting or reject a transform in progress','LO'),(54,10,'State that the length of the dashed line controls the applied scale factor','LO'),(55,10,'When scaling, select an appropriate position for the mouse before beginning','SC'),(56,11,'Use various viewing angles to easily constrain translation and rotation to a plane','SC'),(57,11,'State how to constrain a transform to apply to a single global axis only','LO'),(58,11,'State how, using the keyboard, to constrain a translation or scale transform to a plane (two axes at once)','LO'),(59,11,'Successfully constrain translation, rotation and scale transforms using the keyboard','SC'),(60,11,'Be aware that a local, or internal set of axes may differ from the global axes (typically after rotation)','LO'),(61,11,'Transform an object by giving exact numeric values via the keyboard','SC'),(62,11,'Transform an object over discrete intervals using the CTRL key and mouse drag','SC'),(63,11,'State how to use the keyboard and mouse to give discrete transformations','LO'),(64,12,'Locate and edit the object properties relating to location, rotation and scale','SC'),(65,12,'Know that object transform properties can be directly edited in the object properties area','LO'),(66,12,'Understand the effect of clearing transformation data using the Object menu in the 3D viewport','LO'),(67,12,'Understand the effect of applying transformation data using the Object menu in the 3D viewport','LO'),(68,12,'Describe the effect of applying rotation data to a rotated object, with regard to local axes constraints','SC'),(69,13,'Know that the framerate is the number of frames per second','LO'),(70,13,'Change animation framerate to 30 fps','SC'),(71,13,'Calculate the number of frames required for animation to have particular duration in seconds','LO'),(72,13,'Correctly set the timeline to stop animation after a set number of frames','SC'),(73,14,'Correctly use \"frame, position, select, insert keyframe\" sequence to set up and insert a keyframe','SC'),(74,14,'Know that objects to be keyframed should be selected, before pressing I to insert keyframe','LO'),(75,14,'Know that various properties of an object can be keyframed','LO'),(76,14,'Create a simple animation using two or more objects, with two or more keyframes','SC'),(77,14,'Explain the meaning of interpolation between keyframes','LO'),(78,15,'Use the timeline controls to play, stop, rewind and jump between keyframes','SC'),(79,15,'Know that the timeline controls permit backwards play and keyframe hops','LO'),(80,15,'Use mouse scrubbing in the timeline to check over an animation','SC'),(81,15,'Explain why scrubbing functionality dictates that you must first select the required frame before trying to set up object positions for keyframing','LO');
/*!40000 ALTER TABLE `outcome_learningintentiondetail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_answer`
--

DROP TABLE IF EXISTS `quiz_answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_answer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `answer_text` longtext NOT NULL,
  `explan_text` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_answer`
--

LOCK TABLES `quiz_answer` WRITE;
/*!40000 ALTER TABLE `quiz_answer` DISABLE KEYS */;
/*!40000 ALTER TABLE `quiz_answer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_question`
--

DROP TABLE IF EXISTS `quiz_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_text` longtext NOT NULL,
  `correct_answer_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `correct_answer_id_refs_id_2a462f47` (`correct_answer_id`),
  CONSTRAINT `correct_answer_id_refs_id_2a462f47` FOREIGN KEY (`correct_answer_id`) REFERENCES `quiz_answer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_question`
--

LOCK TABLES `quiz_question` WRITE;
/*!40000 ALTER TABLE `quiz_question` DISABLE KEYS */;
/*!40000 ALTER TABLE `quiz_question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_question_answers`
--

DROP TABLE IF EXISTS `quiz_question_answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_question_answers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) NOT NULL,
  `answer_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `question_id` (`question_id`,`answer_id`),
  KEY `answer_id_refs_id_53c80bb5` (`answer_id`),
  CONSTRAINT `answer_id_refs_id_53c80bb5` FOREIGN KEY (`answer_id`) REFERENCES `quiz_answer` (`id`),
  CONSTRAINT `question_id_refs_id_39f2d869` FOREIGN KEY (`question_id`) REFERENCES `quiz_question` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_question_answers`
--

LOCK TABLES `quiz_question_answers` WRITE;
/*!40000 ALTER TABLE `quiz_question_answers` DISABLE KEYS */;
/*!40000 ALTER TABLE `quiz_question_answers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_questionattempt`
--

DROP TABLE IF EXISTS `quiz_questionattempt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_questionattempt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `quiz_attempt_id` int(11) NOT NULL,
  `question_id` int(11) NOT NULL,
  `answer_given_id` int(11) NOT NULL,
  `score` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `question_id_refs_id_a05ab6b` (`question_id`),
  KEY `quiz_attempt_id_refs_id_1d79080e` (`quiz_attempt_id`),
  KEY `answer_given_id_refs_id_650047e1` (`answer_given_id`),
  CONSTRAINT `answer_given_id_refs_id_650047e1` FOREIGN KEY (`answer_given_id`) REFERENCES `quiz_answer` (`id`),
  CONSTRAINT `question_id_refs_id_a05ab6b` FOREIGN KEY (`question_id`) REFERENCES `quiz_question` (`id`),
  CONSTRAINT `quiz_attempt_id_refs_id_1d79080e` FOREIGN KEY (`quiz_attempt_id`) REFERENCES `quiz_quizattempt` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_questionattempt`
--

LOCK TABLES `quiz_questionattempt` WRITE;
/*!40000 ALTER TABLE `quiz_questionattempt` DISABLE KEYS */;
/*!40000 ALTER TABLE `quiz_questionattempt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_quiz`
--

DROP TABLE IF EXISTS `quiz_quiz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_quiz` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `quiz_title` varchar(200) NOT NULL,
  `lesson_id` int(11) NOT NULL,
  `create_date` date NOT NULL,
  `author_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id_refs_id_1e04f0b4` (`author_id`),
  KEY `lesson_id_refs_id_4aecb232` (`lesson_id`),
  CONSTRAINT `author_id_refs_id_1e04f0b4` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `lesson_id_refs_id_4aecb232` FOREIGN KEY (`lesson_id`) REFERENCES `courses_lesson` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_quiz`
--

LOCK TABLES `quiz_quiz` WRITE;
/*!40000 ALTER TABLE `quiz_quiz` DISABLE KEYS */;
/*!40000 ALTER TABLE `quiz_quiz` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_quiz_questions`
--

DROP TABLE IF EXISTS `quiz_quiz_questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_quiz_questions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `quiz_id` int(11) NOT NULL,
  `question_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `quiz_id` (`quiz_id`,`question_id`),
  KEY `question_id_refs_id_296a745a` (`question_id`),
  CONSTRAINT `question_id_refs_id_296a745a` FOREIGN KEY (`question_id`) REFERENCES `quiz_question` (`id`),
  CONSTRAINT `quiz_id_refs_id_424a03fb` FOREIGN KEY (`quiz_id`) REFERENCES `quiz_quiz` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_quiz_questions`
--

LOCK TABLES `quiz_quiz_questions` WRITE;
/*!40000 ALTER TABLE `quiz_quiz_questions` DISABLE KEYS */;
/*!40000 ALTER TABLE `quiz_quiz_questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_quizattempt`
--

DROP TABLE IF EXISTS `quiz_quizattempt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_quizattempt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `quiz_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `taken_dt` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id_refs_id_2454cd5c` (`user_id`),
  KEY `quiz_id_refs_id_e5ec5c3` (`quiz_id`),
  CONSTRAINT `quiz_id_refs_id_e5ec5c3` FOREIGN KEY (`quiz_id`) REFERENCES `quiz_quiz` (`id`),
  CONSTRAINT `user_id_refs_id_2454cd5c` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_quizattempt`
--

LOCK TABLES `quiz_quizattempt` WRITE;
/*!40000 ALTER TABLE `quiz_quizattempt` DISABLE KEYS */;
/*!40000 ALTER TABLE `quiz_quizattempt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registration_registrationprofile`
--

DROP TABLE IF EXISTS `registration_registrationprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registration_registrationprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `activation_key` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_313280c4` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registration_registrationprofile`
--

LOCK TABLES `registration_registrationprofile` WRITE;
/*!40000 ALTER TABLE `registration_registrationprofile` DISABLE KEYS */;
INSERT INTO `registration_registrationprofile` VALUES (2,17,'21fb58d07fbf12be2a38d4a55352262ce054681a'),(3,18,'f0c35bcc54041f10ef73451b7c6078eed52e11c6'),(4,19,'eae85ccb4426867d23ef75f869f4f44b2f05ee05'),(5,20,'ALREADY_ACTIVATED'),(6,21,'c3ef57c73ea53c8910539b261a496a3070fe0384'),(7,22,'ALREADY_ACTIVATED'),(8,23,'ALREADY_ACTIVATED');
/*!40000 ALTER TABLE `registration_registrationprofile` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-07-12  0:29:18
