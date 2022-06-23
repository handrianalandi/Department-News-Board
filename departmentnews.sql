-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 23, 2022 at 07:20 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `departmentnews`
--

-- --------------------------------------------------------

--
-- Table structure for table `file`
--

CREATE TABLE `file` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `file`
--

INSERT INTO `file` (`id`, `name`, `location`) VALUES
(35, 'test.png', 'file/test.png'),
(36, 'test.png', 'file/test.png'),
(37, 'test.png', 'file/test.png'),
(38, 'test.png', 'file/test.png'),
(39, 'test.png', 'file/test.png'),
(40, 'test.png', 'file/test.png'),
(41, 'test.png', 'file/test.png'),
(42, 'test.png', 'file/test.png'),
(43, 'test.png', 'file/test.png'),
(44, 'test.png', 'file/test.png'),
(45, 'test.png', 'file/test.png'),
(46, 'test.png', 'file/test.png'),
(47, 'test123.png', 'file/test123.png'),
(48, 'test121233.png', 'file/test121233.png'),
(49, 'test121123233.png', 'file/test121123233.png'),
(50, 'testgambaranjeng', 'file/<function filename at 0x0000016E0BBDE050>2022-06-23 223830.png'),
(51, 'testgambaranjeng', 'file/testgambaranjeng2022-06-23 234249.png');

-- --------------------------------------------------------

--
-- Table structure for table `news`
--

CREATE TABLE `news` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `title` varchar(50) NOT NULL,
  `content` varchar(500) NOT NULL,
  `date` date NOT NULL,
  `file_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `news`
--

INSERT INTO `news` (`id`, `user_id`, `title`, `content`, `date`, `file_id`) VALUES
(25, 2, 'title1', 'contentupdatekedua1', '2022-06-23', 47),
(26, 2, 'title1', 'content1', '0000-00-00', 48),
(27, 2, 'title1', 'content1', '0000-00-00', 49),
(28, 2, 'title1', 'content1', '0000-00-00', 50),
(29, 2, 'title1', 'content1', '0000-00-00', NULL),
(30, 2, 'title1', 'content1', '2022-06-23', NULL),
(31, 2, 'title1withfile', 'content1withfile', '2022-06-23', 51);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`) VALUES
(1, 'han', 'han123'),
(2, 'han1', 'han123'),
(3, 'han123', 'han123'),
(5, 'han45', 'han123');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `file`
--
ALTER TABLE `file`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `news`
--
ALTER TABLE `news`
  ADD PRIMARY KEY (`id`),
  ADD KEY `file_id` (`file_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `file`
--
ALTER TABLE `file`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT for table `news`
--
ALTER TABLE `news`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `news`
--
ALTER TABLE `news`
  ADD CONSTRAINT `news_ibfk_1` FOREIGN KEY (`file_id`) REFERENCES `file` (`id`),
  ADD CONSTRAINT `news_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);
COMMIT;
