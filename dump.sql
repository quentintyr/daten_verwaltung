-- --------------------------------------------------------
-- Host:                         localhost
-- Server Version:               11.1.2-MariaDB - mariadb.org binary distribution
-- Server Betriebssystem:        Win64
-- HeidiSQL Version:             12.3.0.6589
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Exportiere Datenbank Struktur für daten_verwaltung
CREATE DATABASE IF NOT EXISTS `daten_verwaltung` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;
USE `daten_verwaltung`;

-- Exportiere Struktur von Tabelle daten_verwaltung.adressenverwaltung
CREATE TABLE IF NOT EXISTS `adressenverwaltung` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `FIRMEN_NAME` varchar(50) DEFAULT NULL,
  `NACHNAME` varchar(50) DEFAULT NULL,
  `VORNAMEN` varchar(50) DEFAULT '0',
  `TITEL_1` varchar(50) DEFAULT NULL,
  `TITEL_2` varchar(50) DEFAULT NULL,
  `TITEL_3` varchar(50) DEFAULT NULL,
  `LAND` varchar(50) DEFAULT NULL,
  `LKZ` varchar(50) DEFAULT NULL,
  `STRASSE` varchar(50) DEFAULT '0',
  `HAUS_NR` varchar(50) DEFAULT '0',
  `PLZ` varchar(50) DEFAULT NULL,
  `ORT` varchar(50) DEFAULT '0',
  `MOBIL_NR` varchar(50) DEFAULT '0',
  `BUSINESS_NR` varchar(50) DEFAULT '0',
  `EMAIL` varchar(50) DEFAULT '0',
  `SCHEIN` tinyint(4) DEFAULT NULL,
  `ART` varchar(50) DEFAULT NULL,
  `KINDER` int(11) DEFAULT NULL,
  `GEBURTSDATUM` date DEFAULT NULL,
  `SVNR` varchar(50) DEFAULT NULL,
  `KARTE_NR` varchar(50) DEFAULT NULL,
  `PERSO_NR` varchar(50) DEFAULT NULL,
  `DATETIME` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `NACHNAME` (`NACHNAME`),
  KEY `VORNAMEN` (`VORNAMEN`),
  KEY `FIRMEN_NAME` (`FIRMEN_NAME`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Exportiere Daten aus Tabelle daten_verwaltung.adressenverwaltung: ~1 rows (ungefähr)
INSERT INTO `adressenverwaltung` (`ID`, `FIRMEN_NAME`, `NACHNAME`, `VORNAMEN`, `TITEL_1`, `TITEL_2`, `TITEL_3`, `LAND`, `LKZ`, `STRASSE`, `HAUS_NR`, `PLZ`, `ORT`, `MOBIL_NR`, `BUSINESS_NR`, `EMAIL`, `SCHEIN`, `ART`, `KINDER`, `GEBURTSDATUM`, `SVNR`, `KARTE_NR`, `PERSO_NR`, `DATETIME`) VALUES
	(20, 'KNAPP', 'Wagner', 'Quentin Tyr', '', '', '', 'Austria', 'A  ', 'Josef Hartmann Gasse', '14a', '8075', 'Hart bei Graz', '06781218891', '', 'quentin.wagner@live.at', 0, '', 0, '2003-06-03', '5978', '14142', '8898', '2023-11-17 10:30:53');

-- Exportiere Struktur von Tabelle daten_verwaltung.changelog_table
CREATE TABLE IF NOT EXISTS `changelog_table` (
  `entry_id` int(11) NOT NULL AUTO_INCREMENT,
  `field_changed` varchar(50) DEFAULT NULL,
  `old_value` varchar(50) DEFAULT NULL,
  `new_value` varchar(50) DEFAULT NULL,
  `change_time` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`entry_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=222 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Exportiere Daten aus Tabelle daten_verwaltung.changelog_table: ~0 rows (ungefähr)

-- Exportiere Struktur von Tabelle daten_verwaltung.länder
CREATE TABLE IF NOT EXISTS `länder` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `LAND` varchar(40) NOT NULL,
  `LKZ` varchar(3) NOT NULL,
  `VORWAHL` varchar(50) NOT NULL,
  `EU_JN` varchar(1) NOT NULL,
  `UID_LKZ` varchar(3) NOT NULL,
  `INTRA_STAT_JN` varchar(1) NOT NULL,
  `ZUS_MELDUNG_JN` varchar(1) NOT NULL,
  `UL_KZ` varchar(2) NOT NULL,
  `LANDES_SPRACHE` varchar(2) NOT NULL,
  `LANDES_WÄHRUNG` varchar(2) NOT NULL,
  `DATUM` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`ID`),
  KEY `LAND` (`LAND`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Exportiere Daten aus Tabelle daten_verwaltung.länder: ~6 rows (ungefähr)
INSERT INTO `länder` (`ID`, `LAND`, `LKZ`, `VORWAHL`, `EU_JN`, `UID_LKZ`, `INTRA_STAT_JN`, `ZUS_MELDUNG_JN`, `UL_KZ`, `LANDES_SPRACHE`, `LANDES_WÄHRUNG`, `DATUM`) VALUES
	(1, 'Austria                             ', 'A  ', '+43', 'J', 'ATU', 'J', 'J', 'AT', 'D ', 'EU', '2023-11-16 13:52:36'),
	(2, 'Deutschland                         ', 'D  ', '+49', 'J', 'DE ', 'J', 'J', 'DE', 'D ', 'EU', '2023-11-16 13:52:42'),
	(3, 'England                             ', 'GB ', '+44', 'J', 'GB ', 'J', 'J', 'GB', 'E ', '  ', '2023-11-16 13:53:22'),
	(4, 'Italien                             ', 'I  ', '+39', 'J', 'IT ', 'J', 'J', 'IT', 'I ', 'EU', '2023-11-16 13:53:42'),
	(5, 'Schweiz                             ', 'CH ', '+41', 'N', '   ', 'J', 'N', 'CH', 'D ', '  ', '2023-11-16 13:53:46'),
	(6, 'Ungarn                              ', 'HU ', '+36', 'J', 'HU ', 'J', 'J', 'HU', 'D ', 'EU', '2023-11-16 13:53:58');

-- Exportiere Struktur von Tabelle daten_verwaltung.titel
CREATE TABLE IF NOT EXISTS `titel` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `TITEL` varchar(50) DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Exportiere Daten aus Tabelle daten_verwaltung.titel: ~70 rows (ungefähr)
INSERT INTO `titel` (`ID`, `TITEL`) VALUES
	(3, ''),
	(4, 'Abg.z.NR'),
	(5, 'ADir.'),
	(6, 'AR'),
	(7, 'BA*'),
	(8, 'Bakk. techn.*'),
	(9, 'BBA*'),
	(10, 'Bea.'),
	(11, 'BEd*'),
	(12, 'B.Eng.*'),
	(13, 'Bgm.'),
	(14, 'Bmstr.'),
	(15, 'B.phil'),
	(16, 'BSc*'),
	(17, 'Dr. / Dres.'),
	(18, 'DDr.'),
	(19, 'Dr. h.c.'),
	(20, 'Dr. iur.'),
	(21, 'Dr. med.univ.'),
	(22, 'Dr. med.vet.'),
	(23, 'Dr. mont.'),
	(24, 'Dr. phil.'),
	(25, 'Dr. rer.nat.techn.'),
	(26, 'Dr. rer.pol.'),
	(27, 'Dr. rer.soc.oec.'),
	(28, 'Dr. techn.'),
	(29, 'Dr. theol.'),
	(30, 'Dipl.-Chem.'),
	(31, 'Dipl.-Dolm.'),
	(32, 'Dipl.-Gwl'),
	(33, 'Dipl.-Hdl.'),
	(34, 'Dipl.-HLFL-Ing.'),
	(35, 'Dipl.Holzw.'),
	(36, 'Dipl.-Ing., DI'),
	(37, 'Dipl.-Ing. (FH)'),
	(38, 'Dipl.-Päd.'),
	(39, 'Dir.'),
	(41, 'EMHRD*'),
	(42, 'Gem. R.'),
	(43, 'GR'),
	(44, 'Hon.Prof.'),
	(45, 'HR'),
	(46, 'Ing.'),
	(47, 'KommR'),
	(48, 'LL.B. oder LLB*'),
	(49, 'LL.M. oder LLM*'),
	(50, 'Mag. '),
	(51, 'Maga.'),
	(52, 'MA*'),
	(53, 'Mag. (FH)'),
	(54, 'Mag. arch.'),
	(55, 'Mag. iur.'),
	(56, 'Mag. pharm.'),
	(57, 'Mag. phil.'),
	(58, 'Mag. rer.nat.'),
	(59, 'Mag. rer.soc.oec.'),
	(60, 'Mag. theol.'),
	(61, 'M.A.I.S.*'),
	(62, 'MBA*'),
	(63, 'MedR'),
	(64, 'MIB*'),
	(65, 'Parl. R'),
	(66, 'MSc*'),
	(67, 'PhD'),
	(68, 'Prof.'),
	(69, 'StSekr.'),
	(70, 'Univ.-Ass., Univ.Ass'),
	(71, 'Univ.-Doz., Univ.Doz.'),
	(72, 'Univ.-Lekt., Univ.Lekt.'),
	(73, 'Univ.-Prof., Univ.Prof.');

-- Exportiere Struktur von Tabelle daten_verwaltung.voreinstellungen
CREATE TABLE IF NOT EXISTS `voreinstellungen` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `DARKMODE` tinyint(4) DEFAULT NULL,
  `SPRACHE` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Exportiere Daten aus Tabelle daten_verwaltung.voreinstellungen: ~1 rows (ungefähr)
INSERT INTO `voreinstellungen` (`ID`, `DARKMODE`, `SPRACHE`) VALUES
	(1, 0, 1);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
