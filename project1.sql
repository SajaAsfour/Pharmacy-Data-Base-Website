CREATE DATABASE PharmacyManagement;
USE PharmacyManagement;
CREATE TABLE Customer (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    #address
    city VARCHAR(100),
    street varchar (100),
    DateOfBirth DATE,
    Email VARCHAR(100),
    Phonenum VARCHAR(100)
);

CREATE TABLE CustomerPurchase (
    PurchaseID INT PRIMARY KEY AUTO_INCREMENT,
    CustomerID INT,
    ProductName VARCHAR(100) NOT NULL,
    PurchaseDate DATE NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE
);

CREATE TABLE Pharmacist (
    PharmacistID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    ContactInfo VARCHAR(50),
    Role VARCHAR(50),
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL
);

CREATE TABLE Product (
    ProductID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Description TEXT,
    StockQuantity INT DEFAULT 0,
    Price DECIMAL(10, 2) NOT NULL,
    ExpirationDate DATE,
    ProductType ENUM('Medication', 'Cosmetic') NOT NULL -- Distinguishes between types
);

CREATE TABLE Inventory (
    InventoryID INT PRIMARY KEY AUTO_INCREMENT,
    ProductID INT,
    Quantity INT DEFAULT 0 NOT NULL,
    LastUpdatedDate DATE NOT NULL,
    FOREIGN KEY (ProductID) REFERENCES product(ProductID) ON DELETE CASCADE
);

CREATE TABLE SalesTransaction (
    TransactionID INT PRIMARY KEY AUTO_INCREMENT,
    Date DATE NOT NULL,
    TotalAmount DECIMAL(10, 2) NOT NULL,
    PaymentMethod VARCHAR(50),
    CustomerID INT,
    PharmacistID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE SET NULL,
    FOREIGN KEY (PharmacistID) REFERENCES Pharmacist(PharmacistID) ON DELETE SET NULL
);

CREATE TABLE TransactionItem (
    TransactionItemID INT PRIMARY KEY AUTO_INCREMENT,
    TransactionID INT NOT NULL,
    ProductID INT ,
    Quantity INT NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (TransactionID) REFERENCES SalesTransaction(TransactionID) ON DELETE CASCADE,
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID) ON DELETE SET NULL
);

INSERT INTO Customer (Name, city, street, DateOfBirth, Email, Phonenum)
VALUES
('Ahmad Khalil', 'Gaza City', 'Al-Rasheed Street', '1990-02-15', 'ahmad.khalil@example.com', '0599123456'),
('Fatima Abu Omar', 'Nablus', 'Al-Jabal Street', '1985-07-10', 'fatima.abuomar@example.com', '0598234567'),
('Hussein Saleh', 'Hebron', 'Wadi Al-Tuffah Street', '1978-12-01', 'hussein.saleh@example.com', '0598345678'),
('Mariam Al-Hajj', 'Jericho', 'Ein Al-Sultan Street', '1995-05-20', 'mariam.hajj@example.com', '0598456789'),
('Yousef Taha', 'Ramallah', 'Al-Balou Street', '1982-03-30', 'yousef.taha@example.com', '0598567890'),
('Layla Saeed', 'Jenin', 'Al-Marah Street', '1992-11-15', 'layla.saeed@example.com', '0598678901'),
('Khaled Naser', 'Gaza City', 'Al-Shifa Street', '1980-06-25', 'khaled.naser@example.com', '0598789012'),
('Hala Zayed', 'Bethlehem', 'Manger Street', '1988-01-18', 'hala.zayed@example.com', '0598890123'),
('Ali Hassan', 'Tulkarm', 'Al-Quds Street', '1975-09-05', 'ali.hassan@example.com', '0598901234'),
('Nour Mansour', 'Qalqilya', 'Al-Salam Street', '1993-08-22', 'nour.mansour@example.com', '0599012345');

UPDATE Customer
SET Email = 'nour.mansour@gmail.com'
WHERE CustomerID = 10;

select * from customer;

INSERT INTO CustomerPurchase (CustomerID, ProductName, PurchaseDate)
VALUES
(1, 'Aspirin', '2024-01-15'),
(1, 'Paracetamol', '2024-01-16'),
(2, 'Lipstick', '2024-01-20'),
(2, 'Moisturizer', '2024-01-25'),
(3, 'Amoxicillin', '2024-02-05'),
(3, 'Perfume', '2024-02-10'),
(4, 'Vitamins', '2024-02-15'),
(5, 'Cough Syrup', '2024-02-20'),
(6, 'Cold Tablets', '2024-02-22'),
(7, 'Antiseptic Cream', '2024-02-25');

select * from CustomerPurchase;


INSERT INTO Product (Name, Description, StockQuantity, Price, ExpirationDate, ProductType)
VALUES
-- Medications
('ZITROCIN', 'Upper respiratory tract infection', 200, 40, '2025-10-15', 'Medication'),
('AZIMEX', 'Upper respiratory tract infection', 150, 42, '2025-12-30', 'Medication'),
('Azicare', 'Upper respiratory tract infection', 300, 40, '2025-06-10', 'Medication'),
('Aziro', 'Upper respiratory tract infection', 100, 22, '2025-03-20', 'Medication'),
('Dexamol', 'pain relief and fever reduction', 120, 28, '2025-07-30', 'Medication'),
('Sedamol', 'pain relief and fever reduction', 400, 10, '2026-01-01', 'Medication'),
('Acamol', 'pain relief and fever reduction', 180, 13, '2025-11-25', 'Medication'),
('Panadol', 'pain relief and fever reduction', 90, 14, '2025-10-15', 'Medication'),
('Advil Fort', 'pain relief and reducing inflammation', 250, 49, '2025-12-01', 'Medication'),
('IBUFEN', 'pain relief and reducing inflammation', 140,32, '2025-08-20', 'Medication'),
('TRUFEN', 'Topical gel for pain relief', 140,15, '2025-09-20', 'Medication'),
('VALZAN-HCT', 'Manages high blood pressure', 146,26, '2025-08-02', 'Medication'),
('Diovan', 'Manages high blood pressure', 110,28, '2025-10-17', 'Medication'),
('CLAMOXIN BID', 'treat bacterial infections', 146,38, '2025-12-12', 'Medication'),
('AMOXICLAV', 'treat bacterial infections', 80,37, '2025-04-20', 'Medication'),
('Augmentin', 'treat bacterial infections', 140,37, '2025-07-14', 'Medication'),
('LIPONIL', 'manage high cholesterol levels and triglycerides', 140,49, '2025-08-20', 'Medication'),
('LIPIDEX', 'manage high cholesterol levels and triglycerides', 200,45, '2025-08-29', 'Medication'),
('Lipitor', 'manage high cholesterol levels and triglycerides', 140,54, '2025-08-20', 'Medication'),
('ROSULIP', 'manage high cholesterol levels and triglycerides', 140,80, '2025-08-20', 'Medication'),
('Crestor', 'manage high cholesterol levels and triglycerides', 140,99, '2025-08-20', 'Medication'),
('ANAPRIL', 'treat conditions related to the heart and blood vessels', 140,25, '2025-08-20', 'Medication'),
('ENALADEX', 'treat conditions related to the heart and blood vessels', 140,15, '2025-08-20', 'Medication'),
('Lucast', 'Relieves symptoms of seasonal allergies and allergic rhinitis', 140,65, '2025-08-20', 'Medication'),
('SINGULAIR', 'Relieves symptoms of seasonal allergies and allergic rhinitis', 140,81, '2025-08-20', 'Medication'),
('LEUKOMONT4MG CHEWABEL TABLETS', 'Relieves symptoms of seasonal allergies and allergic rhinitis', 140,67, '2025-08-20', 'Medication'),
('Rhinofex', 'nasal congestion', 140,20, '2025-08-20', 'Medication'),
('Otrivin', 'nasal congestion', 140,32, '2025-08-20', 'Medication'),
('Candistan', 'treat a variety of fungal infections', 140,14, '2025-08-20', 'Medication'),
('Canesten', 'treat a variety of fungal infections', 140,41, '2025-08-20', 'Medication'),

-- Cosmetic Products
('LABELLO LIPSTICK', 'Lipstick', 50, 10, '2026-03-15', 'Cosmetic'),
('JOKO MATT LIPS LIPSTICK', 'Lipstick', 30, 15, '2026-07-15', 'Cosmetic'),
('MUSIC FLOWER ULTRA VELVET MATTE LIPSTICk', 'Lipstick', 80, 15, '2026-07-15', 'Cosmetic'),
('YOKO HEALTHY WHITE MOISTURIZER CREAM', 'Hydrating skin moisturizer', 90, 45, '2025-11-20', 'Cosmetic'),
('NEUTROGENA HYDRO BOOST GEL CREAM, DRY SKIN', 'Hydrating skin moisturizer', 100, 55, '2025-12-20', 'Cosmetic'),
('BIODERM ATODERM GEL CREAM, DRY SKIN', 'Hydrating skin moisturizer', 100, 75, '2026-04-20', 'Cosmetic'),
('INSPIRE PERFUMED SPRAY', 'body spray', 30, 25, '2027-08-01', 'Cosmetic'),
('MINI CRYSTAL PERFUMED', 'body spray', 20, 25, '2027-09-01', 'Cosmetic'),
('MAISON ALHAMBRA EXTRA LONG LASING PERFUMED BODY SPRAY', 'body spray', 40, 25, '2027-08-01', 'Cosmetic'),
('BIODERM Sunscreen', 'Sunscreen', 60, 80, '2025-04-15', 'Cosmetic'),
('Avene Sunscreen', 'Sunscreen', 60, 110, '2025-08-15', 'Cosmetic'),
('Nextgen SPF Sunscreen', 'Sunscreen', 60, 90, '2025-07-15', 'Cosmetic'),
('TOPFACE Foundation', 'Foundation', 40, 35, '2026-09-30', 'Cosmetic'),
('TONY MAKE UP FOR YOU HD PROFESSIONAL FOUNDATION', 'Foundation', 30, 50, '2026-09-30', 'Cosmetic'),
('OSHEA Foundation', 'Foundation', 30, 55, '2026-09-30', 'Cosmetic'),
('BIODERM Face Wash', 'Face Wash', 100, 110, '2025-06-05', 'Cosmetic'),
('Avene Face Wash', 'Face Wash', 100, 80, '2025-06-05', 'Cosmetic'),
('NIVEA CLEANSE & CARE FACE WASH', 'Face Wash', 100, 70, '2025-06-05', 'Cosmetic'),
('CHI ROYAL SHAMPOO', 'shampoo', 120, 100, '2026-01-20', 'Cosmetic'),
('ALASEEL COSMETICS HAIR SHAMPOO', 'shampoo', 80, 90, '2026-01-20', 'Cosmetic'),
('BABY SEBAMED SHAMPOO', 'shampoo', 120, 100, '2026-12-20', 'Cosmetic'),
('LANA LINE HELLO BEAUTIFUL HAND CREAM', 'hand cream', 80, 150, '2026-03-10', 'Cosmetic'),
('LOVINA CARE TREAT HAND CREAM', 'hand cream', 80, 35, '2026-03-10', 'Cosmetic'),
('ESFOLIO FRESH PINK PEACH HAND CREAM', 'hand cream', 80, 70, '2026-03-10', 'Cosmetic'),
('TO-ME JOJOBA EXTRACT BODY LOTION', 'body lotion', 90,110, '2025-11-15', 'Cosmetic'),
('NIVEA NATURAL GLOW C&A VITAMIN BODY LOTION', 'body lotion', 90,75, '2025-11-15', 'Cosmetic'),
('VASU SHEA BUTTER CARE BODY LOTION', 'body lotion', 90,130, '2025-11-15', 'Cosmetic'),

('Vitamin D3', 'Vitamin', 100, 36, '2026-02-01', 'Medication'),
('Vitamin B12', 'Vitamin', 90, 28, '2028-02-01', 'Medication'),
('Vitamin C', 'Vitamin', 70, 41, '2026-12-01', 'Medication'),
('VATIKA ONION ENRICHED HAIR OIL', 'Hair Oil', 60, 35, '2026-06-15', 'Cosmetic'),
('KISS BEAUTY HAIR OIL', 'Hair Oil', 60, 25, '2026-10-15', 'Cosmetic'),
('PURE HAIR OIL', 'Hair Oil', 60, 100, '2026-06-15', 'Cosmetic'),
('ULTRA MAX', 'Deodorant', 140, 20, '2026-05-25', 'Cosmetic'),
('DOVE', 'Deodorant', 140, 18, '2025-05-25', 'Cosmetic'),
('HUGO Deodorant', 'Deodorant', 140, 45, '2028-05-25', 'Cosmetic'),
('SUN GEL LOLO PLUS HAND SANITIZER', 'Hand Sanitizer', 50, 30, '2025-03-01', 'Cosmetic'),
('HIGEEN ANTI-BACTERIAL HAND SANITIZER', 'Hand Sanitizer', 100, 10, '2027-03-01', 'Cosmetic'),
('MIX HAND SANITIZER GEL', 'Hand Sanitizer', 200, 15, '2025-03-01', 'Cosmetic'),
('ORAL-B PRO-EXPERT DEEP CLEAN TOOTHPASTE', 'Toothpaste', 90, 15, '2026-07-05', 'Cosmetic'),
('SIGNAL COMPLETE Toothpaste', 'Toothpaste', 60, 14, '2026-07-05', 'Cosmetic'),
('WHITE GLO PROFESSIONAL CHOICE TOOTHPASTE', 'Toothpaste', 80, 27, '2026-07-05', 'Cosmetic');

select * from product;

INSERT INTO Pharmacist (Name, ContactInfo, Role, Username, Password)
VALUES
('Areej Shrateh', '0598567165', 'Senior Pharmacist', 'ashrateh', 'Areej456'),
('Asem Rimawi', '0598567166', 'Senior Pharmacist', 'arimawi', 'Asem456'),
('Sarah Hassan', '0598123456', 'Pharmacist', 'shassan', 'Sarah123'),
('Ahmad Nasser', '0598234567', 'Pharmacist', 'dnasser', 'Ahmad123'),
('Rania Al-Jamal', '0598345678', 'Pharmacist', 'rjamal', 'Rania123');

select * from Pharmacist;
SELECT COUNT(*) FROM pharmacist where Role = "Pharmacist";
ALTER TABLE Product
DROP COLUMN StockQuantity;

select * from product;
SET SQL_SAFE_UPDATES = 0;
ALTER TABLE Inventory AUTO_INCREMENT = 1;
INSERT INTO Inventory (ProductID, Quantity, LastUpdatedDate)
VALUES
-- Medications
(1, 200, '2024-11-29'),   -- ZITROCIN
(2, 150, '2024-11-29'),   -- AZIMEX
(3, 300, '2024-11-29'),   -- Azicare
(4, 100, '2024-11-29'),   -- Aziro
(5, 120, '2024-11-29'),   -- Dexamol
(6, 400, '2024-11-29'),   -- Sedamol
(7, 180, '2024-11-29'),   -- Acamol
(8, 90, '2024-11-29'),    -- Panadol
(9, 250, '2024-11-29'),   -- Advil Fort
(10, 140, '2024-11-29'),  -- IBUFEN
(11, 140, '2024-11-29'),  -- TRUFEN
(12, 146, '2024-11-29'),  -- VALZAN-HCT
(13, 110, '2024-11-29'),  -- Diovan
(14, 146, '2024-11-29'),  -- CLAMOXIN BID
(15, 80, '2024-11-29'),   -- AMOXICLAV
(16, 140, '2024-11-29'),  -- Augmentin
(17, 140, '2024-11-29'),  -- LIPONIL
(18, 200, '2024-11-29'),  -- LIPIDEX
(19, 140, '2024-11-29'),  -- Lipitor
(20, 140, '2024-11-29'),  -- ROSULIP
(21, 140, '2024-11-29'),  -- Crestor
(22, 140, '2024-11-29'),  -- ANAPRIL
(23, 140, '2024-11-29'),  -- ENALADEX
(24, 140, '2024-11-29'),  -- Lucast
(25, 140, '2024-11-29'),  -- SINGULAIR
(26, 140, '2024-11-29'),  -- LEUKOMONT4MG CHEWABEL TABLETS
(27, 140, '2024-11-29'),  -- Rhinofex
(28, 140, '2024-11-29'),  -- Otrivin
(29, 140, '2024-11-29'),  -- Candistan
(30, 140, '2024-11-29'),  -- Canesten

-- Cosmetic Products
(31, 50, '2024-11-29'),   -- LABELLO LIPSTICK
(32, 30, '2024-11-29'),   -- JOKO MATT LIPS LIPSTICK
(33, 80, '2024-11-29'),   -- MUSIC FLOWER ULTRA VELVET MATTE LIPSTICK
(34, 90, '2024-11-29'),   -- YOKO HEALTHY WHITE MOISTURIZER CREAM
(35, 100, '2024-11-29'),  -- NEUTROGENA HYDRO BOOST GEL CREAM, DRY SKIN
(36, 100, '2024-11-29'),  -- BIODERM ATODERM GEL CREAM, DRY SKIN
(37, 30, '2024-11-29'),   -- INSPIRE PERFUMED SPRAY
(38, 20, '2024-11-29'),   -- MINI CRYSTAL PERFUMED
(39, 40, '2024-11-29'),   -- MAISON ALHAMBRA EXTRA LONG LASING PERFUMED BODY SPRAY
(40, 60, '2024-11-29'),   -- BIODERM Sunscreen
(41, 60, '2024-11-29'),   -- Avene Sunscreen
(42, 60, '2024-11-29'),   -- Nextgen SPF Sunscreen
(43, 40, '2024-11-29'),   -- TOPFACE Foundation
(44, 30, '2024-11-29'),   -- TONY MAKE UP FOR YOU HD PROFESSIONAL FOUNDATION
(45, 30, '2024-11-29'),   -- OSHEA Foundation
(46, 100, '2024-11-29'),  -- BIODERM Face Wash
(47, 100, '2024-11-29'),  -- Avene Face Wash
(48, 100, '2024-11-29'),  -- NIVEA CLEANSE & CARE FACE WASH
(49, 120, '2024-11-29'),  -- CHI ROYAL SHAMPOO
(50, 80, '2024-11-29'),   -- ALASEEL COSMETICS HAIR SHAMPOO
(51, 120, '2024-11-29'),  -- BABY SEBAMED SHAMPOO
(52, 60, '2024-11-29'),   -- VATIKA ONION ENRICHED HAIR OIL
(53, 60, '2024-11-29'),   -- KISS BEAUTY HAIR OIL
(54, 60, '2024-11-29'),   -- PURE HAIR OIL
(55, 140, '2024-11-29'),  -- ULTRA MAX Deodorant
(56, 140, '2024-11-29'),  -- DOVE Deodorant
(57, 140, '2024-11-29'),  -- HUGO Deodorant
(58, 50, '2024-11-29'),   -- SUN GEL LOLO PLUS HAND SANITIZER
(59, 100, '2024-11-29'),  -- HIGEEN ANTI-BACTERIAL HAND SANITIZER
(60, 200, '2024-11-29'),  -- MIX HAND SANITIZER GEL
(61, 90, '2024-11-29'),   -- ORAL-B PRO-EXPERT DEEP CLEAN TOOTHPASTE
(62, 60, '2024-11-29'),   -- SIGNAL COMPLETE Toothpaste
(63, 80, '2024-11-29'),   -- WHITE GLO PROFESSIONAL CHOICE TOOTHPASTE
(64, 100, '2024-11-29'),  -- NIVEA NATURAL GLOW C&A VITAMIN BODY LOTION
(65, 100, '2024-11-29'),  -- VASU SHEA BUTTER CARE BODY LOTION
(66, 90, '2024-11-29'),   -- TO-ME JOJOBA EXTRACT BODY LOTION
(67, 120, '2024-11-29'),  -- LANA LINE HELLO BEAUTIFUL HAND CREAM
(68, 150, '2024-11-29'),  -- LOVINA CARE TREAT HAND CREAM
(69, 80, '2024-11-29'),   -- ESFOLIO FRESH PINK PEACH HAND CREAM
(70, 90, '2024-11-29'),   -- NIVEA HAND CREAM
(71, 80, '2024-11-29'),   -- NEUTROGENA HAND CREAM
(72, 100, '2024-11-29');  -- AVENE HAND CREAM

select * from Inventory;
INSERT INTO SalesTransaction (Date, TotalAmount, PaymentMethod, CustomerID, PharmacistID)
VALUES
('2024-11-29', 120.00, 'Cash', 1, 1),  -- Transaction for Ahmad Khalil, handled by Areej Shrateh
('2024-11-29', 85.50, 'Card', 2, 2),   -- Transaction for Fatima Abu Omar, handled by Asem Rimawi
('2024-11-30', 50.00, 'Cash', 3, 3),   -- Transaction for Hussein Saleh, handled by Sarah Hassan
('2024-11-30', 75.00, 'Card', 4, 4),   -- Transaction for Mariam Al-Hajj, handled by Ahmad Nasser
('2024-12-01', 95.00, 'Cash', 5, 5),   -- Transaction for Yousef Taha, handled by Rania Al-Jamal
('2024-12-01', 120.00, 'Cash', 6, 1),  -- Transaction for Layla Saeed, handled by Areej Shrateh
('2024-12-02', 200.00, 'Card', 7, 2),  -- Transaction for Khaled Naser, handled by Asem Rimawi
('2024-12-02', 55.00, 'Card', 8, 3),   -- Transaction for Hala Zayed, handled by Sarah Hassan
('2024-12-03', 150.00, 'Cash', 9, 4),  -- Transaction for Ali Hassan, handled by Ahmad Nasser
('2024-12-03', 175.00, 'Card', 10, 5); -- Transaction for Nour Mansour, handled by Rania Al-Jamal

select * from SalesTransaction;
ALTER TABLE SalesTransaction AUTO_INCREMENT = 1;
delete from SalesTransaction ;
ALTER TABLE TransactionItem AUTO_INCREMENT = 1;
-- Transaction 1 (Ahmad Khalil)
INSERT INTO TransactionItem (TransactionID, ProductID, Quantity, Price)
VALUES
(1, 1, 2, 40.00),  -- ZITROCIN (2 units)
(1, 4, 1, 28.00);  -- Dexamol (1 unit)

-- Transaction 2 (Fatima Abu Omar)
INSERT INTO TransactionItem (TransactionID, ProductID, Quantity, Price)
VALUES
(2, 2, 2, 42.00),  -- AZIMEX (2 units)
(2, 5, 1, 28.00);  -- Dexamol (1 unit)

-- Transaction 3 (Hussein Saleh)
INSERT INTO TransactionItem (TransactionID, ProductID, Quantity, Price)
VALUES
(3, 3, 1, 40.00),  -- Azicare (1 unit)
(3, 9, 1, 49.00);  -- Advil Fort (1 unit)

-- Transaction 4 (Mariam Al-Hajj)
INSERT INTO TransactionItem (TransactionID, ProductID, Quantity, Price)
VALUES
(4, 12, 1, 26.00),  -- VALZAN-HCT (1 unit)
(4, 15, 2, 37.00);  -- AMOXICLAV (2 units)

-- Transaction 5 (Yousef Taha)
INSERT INTO TransactionItem (TransactionID, ProductID, Quantity, Price)
VALUES
(5, 14, 1, 38.00),  -- CLAMOXIN BID (1 unit)
(5, 17, 1, 49.00);  -- LIPONIL (1 unit)

-- Transaction 6 (Layla Saeed)
INSERT INTO TransactionItem (TransactionID, ProductID, Quantity, Price)
VALUES
(6, 10, 3, 32.00),  -- IBUFEN (3 units)
(6, 19, 1, 54.00);  -- Lipitor (1 unit)

-- Transaction 7 (Khaled Naser)
INSERT INTO TransactionItem (TransactionID, ProductID, Quantity, Price)
VALUES
(7, 13, 1, 28.00),  -- Diovan (1 unit)
(7, 23, 2, 80.00);  -- LIPIDEX (2 units)

-- Transaction 8 (Hala Zayed)
INSERT INTO TransactionItem (TransactionID, ProductID, Quantity, Price)
VALUES
(8, 16, 1, 37.00),  -- Augmentin (1 unit)
(8, 22, 1, 25.00);  -- ENALADEX (1 unit)

-- Transaction 9 (Ali Hassan)
INSERT INTO TransactionItem (TransactionID, ProductID, Quantity, Price)
VALUES
(9, 11, 2, 15.00),  -- TRUFEN (2 units)
(9, 6, 1, 10.00);   -- Sedamol (1 unit)

-- Transaction 10 (Nour Mansour)
INSERT INTO TransactionItem (TransactionID, ProductID, Quantity, Price)
VALUES
(10, 27, 1, 14.00),  -- Rhinofex (1 unit)
(10, 30, 2, 41.00);  -- Canesten (2 units)

select * from TransactionItem;

ALTER TABLE Pharmacist
ADD COLUMN Wage DECIMAL(10, 2) NOT NULL DEFAULT 0.00;

UPDATE Pharmacist
SET Wage = 3000.00
WHERE PharmacistID = 1;

UPDATE Pharmacist
SET Wage = 2800.00
WHERE PharmacistID = 2;

UPDATE Pharmacist
SET Wage = 2500.00
WHERE PharmacistID = 3;

UPDATE Pharmacist
SET Wage = 2700.00
WHERE PharmacistID = 4;

UPDATE Pharmacist
SET Wage = 2600.00
WHERE PharmacistID = 5;

SELECT * FROM Pharmacist;

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY AUTO_INCREMENT,
    PharmacistID INT NOT NULL,
    ProductID INT NOT NULL,
    OrderDate DATE NOT NULL,
    Quantity INT NOT NULL,
    FOREIGN KEY (PharmacistID) REFERENCES Pharmacist(PharmacistID) ON DELETE CASCADE,
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID) ON DELETE CASCADE
);

INSERT INTO Orders (PharmacistID, ProductID, OrderDate, Quantity)
VALUES
(1, 1, '2024-12-01', 50),
(2, 3, '2024-12-02', 30),
(3, 5, '2024-12-03', 100),
(4, 8, '2024-12-04', 40),
(5, 10, '2024-12-05', 20);

SELECT COUNT(*) FROM customer;
INSERT INTO Customer (Name, city, street, DateOfBirth, Email, Phonenum)
VALUES
('Samah Khalil', 'Ramallah', 'Al-Quds Street', '1990-02-15', 'samah@gmail.com', '0598123456');

SELECT 
    SUM(TI.Quantity) AS TotalQuantitySold
FROM 
    SalesTransaction ST
JOIN 
    TransactionItem TI ON ST.TransactionID = TI.TransactionID
WHERE 
    ST.Date = CURDATE();
    
INSERT INTO SalesTransaction (Date, TotalAmount, PaymentMethod, CustomerID, PharmacistID)
VALUES
('2024-12-26', 120.00, 'Cash', 2, 1);

INSERT INTO SalesTransaction (Date, TotalAmount, PaymentMethod, CustomerID, PharmacistID)
VALUES
(CURRENT_DATE, 120.00, 'Cash', 2, 1);

select * from SalesTransaction;
INSERT INTO TransactionItem (TransactionID, ProductID, Quantity, Price)
VALUES
(13, 11, 2, 15.00),  -- TRUFEN (2 units)
(13, 6, 1, 10.00);   -- Sedamol (1 unit)
SELECT * FROM SalesTransaction WHERE Date = '2024-12-26' AND TotalAmount = 120.00;

SELECT SUM(TI.Quantity) AS TotalQuantitySold
FROM SalesTransaction ST
JOIN TransactionItem TI ON ST.TransactionID = TI.TransactionID
WHERE ST.Date = '2024-12-26';

SELECT SUM(TotalAmount) AS TotalRevenue FROM SalesTransaction;

SELECT SUM(TotalAmount) AS TotalRevenue FROM SalesTransaction where date = "2024-12-26";
