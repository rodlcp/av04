-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 14, 2019 at 04:48 AM
-- Server version: 10.4.10-MariaDB
-- PHP Version: 7.3.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `av04`
--

-- --------------------------------------------------------

--
-- Table structure for table `cliente`
--

CREATE TABLE `cliente` (
  `CPF` int(11) NOT NULL,
  `Nome` varchar(50) NOT NULL,
  `Data_nasc` date NOT NULL,
  `Sexo` char(1) DEFAULT NULL,
  `Telefone` varchar(12) NOT NULL,
  `Celular` varchar(12) DEFAULT NULL,
  `Email` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `cliente`
--

INSERT INTO `cliente` (`CPF`, `Nome`, `Data_nasc`, `Sexo`, `Telefone`, `Celular`, `Email`) VALUES
(1, 'Jean', '1994-06-15', 'M', '2198765432', NULL, 'jean@gmasil.com'),
(2, 'Rodrigo', '1996-08-27', 'M', '2123456789', NULL, 'rodrigo@gmail.com'),
(3, 'Mauricio', '1990-01-01', 'M', '2123456789', '', 'Mauricio@labma.ufrj.br');

-- --------------------------------------------------------

--
-- Table structure for table `compra`
--

CREATE TABLE `compra` (
  `ID` int(11) NOT NULL,
  `Cliente` int(11) NOT NULL,
  `Produto` int(11) NOT NULL,
  `Loja` int(11) NOT NULL,
  `Quantidade` float NOT NULL,
  `Preco` float NOT NULL,
  `hora` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `compra`
--

INSERT INTO `compra` (`ID`, `Cliente`, `Produto`, `Loja`, `Quantidade`, `Preco`, `hora`) VALUES
(1, 1, 1, 1, 1, 1000000, '2019-12-13 17:43:48'),
(2, 1, 2, 1, 1, 500000, '2019-12-13 17:43:48'),
(3, 1, 3, 3, 1, 4.5, '2019-12-13 21:16:33');

-- --------------------------------------------------------

--
-- Table structure for table `estoque`
--

CREATE TABLE `estoque` (
  `Loja` int(11) NOT NULL,
  `Produto` int(11) NOT NULL,
  `Quantidade` float UNSIGNED NOT NULL,
  `Preco` float UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `estoque`
--

INSERT INTO `estoque` (`Loja`, `Produto`, `Quantidade`, `Preco`) VALUES
(1, 1, 2, 1000000),
(1, 2, 0, 500000),
(2, 1, 2, 300000),
(3, 3, 9, 4.5);

-- --------------------------------------------------------

--
-- Table structure for table `loja`
--

CREATE TABLE `loja` (
  `CNPJ` int(11) NOT NULL,
  `Nome` varchar(50) NOT NULL,
  `Endereco` varchar(100) NOT NULL,
  `Telefone1` varchar(12) NOT NULL,
  `Telefone2` varchar(12) DEFAULT NULL,
  `Telefone3` varchar(12) DEFAULT NULL,
  `Email` varchar(50) NOT NULL,
  `x` float NOT NULL,
  `y` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `loja`
--

INSERT INTO `loja` (`CNPJ`, `Nome`, `Endereco`, `Telefone1`, `Telefone2`, `Telefone3`, `Email`, `x`, `y`) VALUES
(1, 'LabMA', 'UFRJ', '2123456789', NULL, NULL, 'labma@gmail.com', 10, 7.5),
(2, 'LabMA2', 'UFRJ', '2123456789', NULL, NULL, 'labma2@ufrj.br', 1, -2),
(3, 'Americanas', 'Centro', '2123456789', '', '', 'contato@americanas.com', 7.5, -2.3);

-- --------------------------------------------------------

--
-- Table structure for table `produto`
--

CREATE TABLE `produto` (
  `ID` int(11) NOT NULL,
  `Nome` varchar(50) NOT NULL,
  `Categoria` varchar(20) NOT NULL,
  `Descricao` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `produto`
--

INSERT INTO `produto` (`ID`, `Nome`, `Categoria`, `Descricao`) VALUES
(1, 'Tábua de Mortalidade', 'Tábua', 'Tábuas biométricas de vida da população segurada brasileira'),
(2, 'Tábua de entrada em invalidez', 'Tábua', 'Tábuas biométricas de entrada em invalidez da população segurada brasileira'),
(3, 'Chocolate meio amargo', 'Chocolate', 'Chocolate 40% cacau');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`CPF`);

--
-- Indexes for table `compra`
--
ALTER TABLE `compra`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Cliente` (`Cliente`),
  ADD KEY `Produto` (`Produto`),
  ADD KEY `Loja` (`Loja`);

--
-- Indexes for table `estoque`
--
ALTER TABLE `estoque`
  ADD PRIMARY KEY (`Loja`,`Produto`),
  ADD KEY `Produto` (`Produto`);

--
-- Indexes for table `loja`
--
ALTER TABLE `loja`
  ADD PRIMARY KEY (`CNPJ`);

--
-- Indexes for table `produto`
--
ALTER TABLE `produto`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cliente`
--
ALTER TABLE `cliente`
  MODIFY `CPF` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `compra`
--
ALTER TABLE `compra`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `loja`
--
ALTER TABLE `loja`
  MODIFY `CNPJ` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `produto`
--
ALTER TABLE `produto`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `compra`
--
ALTER TABLE `compra`
  ADD CONSTRAINT `compra_ibfk_1` FOREIGN KEY (`Cliente`) REFERENCES `cliente` (`CPF`) ON DELETE CASCADE,
  ADD CONSTRAINT `compra_ibfk_2` FOREIGN KEY (`Produto`) REFERENCES `produto` (`ID`) ON DELETE CASCADE,
  ADD CONSTRAINT `compra_ibfk_3` FOREIGN KEY (`Loja`) REFERENCES `loja` (`CNPJ`) ON DELETE CASCADE;

--
-- Constraints for table `estoque`
--
ALTER TABLE `estoque`
  ADD CONSTRAINT `estoque_ibfk_1` FOREIGN KEY (`Loja`) REFERENCES `loja` (`CNPJ`) ON DELETE CASCADE,
  ADD CONSTRAINT `estoque_ibfk_2` FOREIGN KEY (`Produto`) REFERENCES `produto` (`ID`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
