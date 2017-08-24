-- phpMyAdmin SQL Dump
-- version 4.6.5.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 24, 2017 at 10:39 PM
-- Server version: 10.1.21-MariaDB
-- PHP Version: 5.6.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `i3m_pharmacy`
--

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(35) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`) VALUES
(1, 'Fatima'),
(2, 'Dalal'),
(3, 'Colla'),
(4, 'Hema'),
(5, 'Mustafa'),
(6, 'Rano'),
(7, 'Khalid'),
(8, 'Omer'),
(9, 'Ahmed'),
(10, 'Hatim'),
(11, 'Amir'),
(12, 'Hamid'),
(13, 'Rania');

-- --------------------------------------------------------

--
-- Table structure for table `exports`
--

CREATE TABLE `exports` (
  `id` int(11) NOT NULL,
  `date` date NOT NULL,
  `destination` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `exports`
--

INSERT INTO `exports` (`id`, `date`, `destination`, `status`) VALUES
(1, '2017-08-08', 'shikan', 'on'),
(3, '2017-08-11', 'destination2', 'status2'),
(4, '2017-08-20', 'Safari', 'on'),
(5, '2017-08-20', 'SUST', 'on'),
(10, '2017-08-20', 'IP', 'on'),
(11, '2017-08-20', 'UDP', 'on'),
(12, '2017-08-20', 'FLAKY', 'on'),
(13, '2017-09-20', 'Diagonal', 'on'),
(14, '2017-08-20', 'Destination', 'off'),
(16, '2017-08-20', 'Destination', 'off'),
(17, '2017-08-20', 'Destination', 'Status'),
(19, '2017-08-20', 'Destination', 'Status'),
(20, '2017-08-20', 'Safari', 'on'),
(22, '2017-08-20', 'Destination', 'Status'),
(23, '2017-08-20', 'Destination', 'Status'),
(24, '2017-08-20', 'Destination', 'Status'),
(25, '2017-08-20', 'Destination', 'Status'),
(26, '2017-08-20', 'Destination', 'Status'),
(27, '2017-08-20', 'Destination', 'Status'),
(28, '2017-08-20', 'Destination', 'Status'),
(29, '2017-08-20', 'Destination', 'Status'),
(30, '2017-08-20', 'Destination', 'Status'),
(31, '2017-08-20', 'Destination', 'Status'),
(32, '2017-08-20', 'Destination', 'Status'),
(33, '2017-08-20', 'Destination', 'Status'),
(34, '2017-08-20', 'Destination', 'Status'),
(35, '2017-08-20', 'Destination', 'Status'),
(36, '2017-08-20', 'Destination', 'Status'),
(37, '2017-08-20', 'Destination', 'Status'),
(38, '2017-08-20', 'Destination', 'Status'),
(39, '2017-08-20', 'Destination', 'Status'),
(40, '2017-08-20', 'Destination', 'Status'),
(41, '2017-08-20', 'Destination', 'Status'),
(42, '2017-08-20', 'Destination', 'Status'),
(43, '2017-08-20', 'Destination', 'Status'),
(44, '2017-08-20', 'Destination', 'Status'),
(45, '2017-08-20', 'Destination', 'Status'),
(46, '2017-08-20', 'MyLife', 'on'),
(48, '2017-08-21', 'Africano', 'good'),
(49, '2017-08-23', 'Destination', 'Status'),
(50, '2017-08-23', 'Destination', 'Status'),
(51, '2017-08-23', 'Destination', 'Status');

-- --------------------------------------------------------

--
-- Table structure for table `export_details`
--

CREATE TABLE `export_details` (
  `id` int(11) NOT NULL,
  `export_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(8) NOT NULL,
  `unitprice` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `export_details`
--

INSERT INTO `export_details` (`id`, `export_id`, `product_id`, `quantity`, `unitprice`) VALUES
(1, 1, 1, 500, 600),
(2, 1, 1, 200, 200),
(3, 1, 1, 100, 100),
(4, 3, 1, 200, 600),
(5, 4, 1, 700, 60),
(6, 10, 1, 8, 80),
(7, 12, 11, 40, 12);

-- --------------------------------------------------------

--
-- Table structure for table `imports`
--

CREATE TABLE `imports` (
  `id` int(11) NOT NULL,
  `receipt_number` varchar(25) NOT NULL,
  `date` date NOT NULL,
  `supplier_id` int(11) NOT NULL,
  `status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `imports`
--

INSERT INTO `imports` (`id`, `receipt_number`, `date`, `supplier_id`, `status`) VALUES
(1, 'mudather', '1995-03-28', 1, 'on'),
(2, 'omg', '2017-08-02', 2, 'on'),
(3, 'Onrails', '2017-08-03', 3, 'on'),
(4, 'google', '2017-08-31', 4, 'on'),
(7, 'ibrahim2312', '2017-08-15', 3, 'on'),
(9, 'snakjd123', '2017-08-24', 3, 'on'),
(10, 'jhsdj1262', '2017-08-23', 3, 'on'),
(11, '9928Ajja', '2017-08-31', 2, 'on'),
(12, '100000', '2017-08-23', 9, 'off'),
(13, 'yahoo', '2017-08-23', 2, 'on'),
(14, '1234', '2017-08-24', 1, 'on');

-- --------------------------------------------------------

--
-- Table structure for table `import_details`
--

CREATE TABLE `import_details` (
  `id` int(11) NOT NULL,
  `import_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(8) NOT NULL,
  `unitprice` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `import_details`
--

INSERT INTO `import_details` (`id`, `import_id`, `product_id`, `quantity`, `unitprice`) VALUES
(1, 1, 1, 200, 10),
(2, 2, 2, 600, 50),
(3, 3, 3, 500, 90),
(4, 4, 4, 70, 5),
(5, 4, 4, 300, 20),
(6, 1, 1, 20, 10),
(7, 12, 12, 600, 12),
(8, 12, 12, 10, 12),
(9, 2, 2, 1, 1),
(10, 11, 11, 1, 1),
(11, 1, 1, 1, 1),
(12, 3, 3, 12, 12),
(13, 3, 3, 50, 1000),
(16, 4, 4, 1232, 123),
(18, 12, 6, 1, 1),
(19, 13, 2, 12, 123),
(20, 4, 11, 12, 12);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `brandname` varchar(25) NOT NULL,
  `genericname` varchar(50) NOT NULL,
  `quantityperunit` varchar(20) NOT NULL,
  `unitprice` float NOT NULL,
  `category_id` int(11) NOT NULL,
  `expiry_date` date NOT NULL,
  `status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `brandname`, `genericname`, `quantityperunit`, `unitprice`, `category_id`, `expiry_date`, `status`) VALUES
(1, 'Glamorous', 'Galaxy', '60', 300, 1, '2017-08-31', 'on'),
(2, 'Homeless', 'Without', '200', 100, 1, '2017-08-21', 'on'),
(3, 'Fatal', 'Error', '1', 100000000, 2, '2017-08-21', 'on'),
(4, 'BlaBlaBla', 'Gosip', '200', 0, 3, '2017-08-31', 'on'),
(5, 'Apple', 'Iphone', '600', 9000, 3, '2017-08-21', 'on'),
(6, 'Yahoo', 'Email', '2', 1, 2, '2017-08-21', 'on'),
(7, 'Malala', 'Nageo', '3', 7, 1, '2017-08-21', 'on'),
(8, 'Magid', 'magdi', '23', 121, 3, '2017-08-21', 'off'),
(9, 'mashroum', 'generic', '8', 1000, 2, '2017-08-21', 'on'),
(11, 'Halk', 'GreenHero', '1', 20000000, 1, '2018-02-28', 'on'),
(12, 'Ibrahim', 'Algadi', '90', 10, 3, '2017-08-31', 'on'),
(13, 'HP	', 'Hewlett Packard', '1', 11000, 5, '2017-11-24', 'on');

-- --------------------------------------------------------

--
-- Table structure for table `suppliers`
--

CREATE TABLE `suppliers` (
  `id` int(11) NOT NULL,
  `name` varchar(25) NOT NULL,
  `address` varchar(40) NOT NULL,
  `contact` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `suppliers`
--

INSERT INTO `suppliers` (`id`, `name`, `address`, `contact`) VALUES
(1, 'Google', 'USA', '0999099909'),
(2, 'Yahoo', 'Khartoum', '0993342343'),
(3, 'Safari', 'Umdormann', '0988288277'),
(4, 'Ibrahim', 'Alnaser', '0993359222'),
(5, 'Mugahid', 'Elaphone', '0993345679'),
(6, 'Mustafa', 'Alnaser', '0992321299'),
(8, 'No Random', 'Sudan', '0990440660'),
(9, 'zxmclkxc', 'asmdms,', '1232132221'),
(11, 'mdlkamslkam', 'alksmdlksa', '1232327657'),
(13, 'this is long text', 'this is long address', '0934567890');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `username` varchar(25) NOT NULL,
  `pssword` varchar(25) NOT NULL,
  `type` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `vouchers`
--

CREATE TABLE `vouchers` (
  `id` int(11) NOT NULL,
  `date` date NOT NULL,
  `submitted_by` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `voucher_details`
--

CREATE TABLE `voucher_details` (
  `voucher_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `exports`
--
ALTER TABLE `exports`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `export_details`
--
ALTER TABLE `export_details`
  ADD PRIMARY KEY (`id`),
  ADD KEY `export_id` (`export_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `imports`
--
ALTER TABLE `imports`
  ADD PRIMARY KEY (`id`),
  ADD KEY `supplier_id` (`supplier_id`);

--
-- Indexes for table `import_details`
--
ALTER TABLE `import_details`
  ADD PRIMARY KEY (`id`),
  ADD KEY `import_id` (`import_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `suppliers`
--
ALTER TABLE `suppliers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `vouchers`
--
ALTER TABLE `vouchers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `voucher_details`
--
ALTER TABLE `voucher_details`
  ADD KEY `voucher_id` (`voucher_id`),
  ADD KEY `product_id` (`product_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
--
-- AUTO_INCREMENT for table `exports`
--
ALTER TABLE `exports`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;
--
-- AUTO_INCREMENT for table `export_details`
--
ALTER TABLE `export_details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- AUTO_INCREMENT for table `imports`
--
ALTER TABLE `imports`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
--
-- AUTO_INCREMENT for table `import_details`
--
ALTER TABLE `import_details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;
--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
--
-- AUTO_INCREMENT for table `suppliers`
--
ALTER TABLE `suppliers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
--
-- AUTO_INCREMENT for table `vouchers`
--
ALTER TABLE `vouchers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `export_details`
--
ALTER TABLE `export_details`
  ADD CONSTRAINT `export_details_ibfk_1` FOREIGN KEY (`export_id`) REFERENCES `exports` (`id`),
  ADD CONSTRAINT `export_details_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

--
-- Constraints for table `imports`
--
ALTER TABLE `imports`
  ADD CONSTRAINT `imports_ibfk_1` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`id`);

--
-- Constraints for table `import_details`
--
ALTER TABLE `import_details`
  ADD CONSTRAINT `import_details_ibfk_1` FOREIGN KEY (`import_id`) REFERENCES `imports` (`id`),
  ADD CONSTRAINT `import_details_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`);

--
-- Constraints for table `voucher_details`
--
ALTER TABLE `voucher_details`
  ADD CONSTRAINT `voucher_details_ibfk_1` FOREIGN KEY (`voucher_id`) REFERENCES `vouchers` (`id`),
  ADD CONSTRAINT `voucher_details_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
