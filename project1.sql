drop database pharmacymanagement;
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

CREATE TABLE Product (
    ProductID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Description TEXT,
    Price DECIMAL(10, 2) NOT NULL,
    ExpirationDate DATE,
    Quantity INT DEFAULT 0 NOT NULL,
    LastUpdatedDate DATE NOT NULL,
    ProductType ENUM('Medication', 'Cosmetic') NOT NULL -- Distinguishes between types
);

CREATE TABLE CustomerPurchase (
    PurchaseID INT PRIMARY KEY AUTO_INCREMENT,
    CustomerID INT,
    ProductID INT,
    PurchaseDate DATE NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE,
	FOREIGN KEY (ProductID) REFERENCES Product(ProductID) ON DELETE CASCADE
);

CREATE TABLE Pharmacist (
    PharmacistID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    ContactInfo VARCHAR(50),
    Role VARCHAR(50),
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Wage DECIMAL(10, 2) NOT NULL DEFAULT 0.00
);

CREATE TABLE Sales (
    SalesID INT PRIMARY KEY AUTO_INCREMENT,
    ProductID INT ,
    Quantity INT NOT NULL,
    Date DATE NOT NULL,
    PaymentMethod VARCHAR(50),
    CustomerID INT,
    PharmacistID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE SET NULL,
    FOREIGN KEY (PharmacistID) REFERENCES Pharmacist(PharmacistID) ON DELETE SET NULL,
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID) ON DELETE SET NULL
);

INSERT INTO Customer (Name, city, street, DateOfBirth, Email, Phonenum)
VALUES
('Ahmad Khalil', 'Gaza City', 'Al-Rasheed Street', '1990-02-15', 'ahmad.khalil@gmail.com', '0599123456'),
('Fatima Abu Omar', 'Nablus', 'Al-Jabal Street', '1985-07-10', 'fatima.abuomar@gmail.com', '0598234567'),
('Hussein Saleh', 'Hebron', 'Wadi Al-Tuffah Street', '1978-12-01', 'hussein.saleh@gmail.com', '0598345678'),
('Mariam Al-Hajj', 'Jericho', 'Ein Al-Sultan Street', '1995-05-20', 'mariam.hajj@gmail.com', '0598456789'),
('Yousef Taha', 'Ramallah', 'Al-Balou Street', '1982-03-30', 'yousef.taha@gmail.com', '0598567890'),
('Layla Saeed', 'Jenin', 'Al-Marah Street', '1992-11-15', 'layla.saeed@gmail.com', '0598678901'),
('Khaled Naser', 'Gaza City', 'Al-Shifa Street', '1980-06-25', 'khaled.naser@gmail.com', '0598789012'),
('Hala Zayed', 'Bethlehem', 'Manger Street', '1988-01-18', 'hala.zayed@gmail.com', '0598890123'),
('Ali Hassan', 'Tulkarm', 'Al-Quds Street', '1975-09-05', 'ali.hassan@gmail.com', '0598901234'),
('Nour Mansour', 'Qalqilya', 'Al-Salam Street', '1993-08-22', 'nour.mansour@gmail.com', '0599012345'),
('Samah Khalil', 'Ramallah', 'Al-Quds Street', '1990-02-15', 'samah@gmail.com', '0598123456');

INSERT INTO Product (Name, Description, Quantity, Price, ExpirationDate, ProductType, LastUpdatedDate)
VALUES
-- Medications
('ZITROCIN', 'Upper respiratory tract infection', 200, 40, '2025-10-15', 'Medication', '2024-11-29'),
('AZIMEX', 'Upper respiratory tract infection', 150, 42, '2025-12-30', 'Medication', '2024-11-29'),
('Azicare', 'Upper respiratory tract infection', 300, 40, '2025-06-10', 'Medication', '2024-11-29'),
('Aziro', 'Upper respiratory tract infection', 100, 22, '2025-03-20', 'Medication', '2024-11-29'),
('Dexamol', 'pain relief and fever reduction', 120, 28, '2025-07-30', 'Medication', '2024-11-29'),
('Sedamol', 'pain relief and fever reduction', 400, 10, '2026-01-01', 'Medication', '2024-11-29'),
('Acamol', 'pain relief and fever reduction', 180, 13, '2025-11-25', 'Medication', '2024-11-29'),
('Panadol', 'pain relief and fever reduction', 90, 14, '2025-10-15', 'Medication', '2024-11-29'),
('Advil Fort', 'pain relief and reducing inflammation', 250, 49, '2025-12-01', 'Medication', '2024-11-29'),
('IBUFEN', 'pain relief and reducing inflammation', 140,32, '2025-08-20', 'Medication', '2024-11-29'),
('TRUFEN', 'Topical gel for pain relief', 140,15, '2025-09-20', 'Medication', '2024-11-29'),
('VALZAN-HCT', 'Manages high blood pressure', 146,26, '2025-08-02', 'Medication', '2024-11-29'),
('Diovan', 'Manages high blood pressure', 110,28, '2025-10-17', 'Medication', '2024-11-29'),
('CLAMOXIN BID', 'treat bacterial infections', 146,38, '2025-12-12', 'Medication', '2024-11-29'),
('AMOXICLAV', 'treat bacterial infections', 80,37, '2025-04-20', 'Medication', '2024-11-29'),
('Augmentin', 'treat bacterial infections', 140,37, '2025-07-14', 'Medication', '2024-11-29'),
('LIPONIL', 'manage high cholesterol levels and triglycerides', 140,49, '2025-08-20', 'Medication', '2024-11-29'),
('LIPIDEX', 'manage high cholesterol levels and triglycerides', 200,45, '2025-08-29', 'Medication', '2024-11-29'),
('Lipitor', 'manage high cholesterol levels and triglycerides', 140,54, '2025-08-20', 'Medication', '2024-11-29'),
('ROSULIP', 'manage high cholesterol levels and triglycerides', 140,80, '2025-08-20', 'Medication', '2024-11-29'),
('Crestor', 'manage high cholesterol levels and triglycerides', 140,99, '2025-08-20', 'Medication', '2024-11-29'),
('ANAPRIL', 'treat conditions related to the heart and blood vessels', 140,25, '2025-08-20', 'Medication', '2024-11-29'),
('ENALADEX', 'treat conditions related to the heart and blood vessels', 140,15, '2025-08-20', 'Medication', '2024-11-29'),
('Lucast', 'Relieves symptoms of seasonal allergies and allergic rhinitis', 140,65, '2025-08-20', 'Medication', '2024-11-29'),
('SINGULAIR', 'Relieves symptoms of seasonal allergies and allergic rhinitis', 140,81, '2025-08-20', 'Medication', '2024-11-29'),
('LEUKOMONT4MG CHEWABEL TABLETS', 'Relieves symptoms of seasonal allergies and allergic rhinitis', 140,67, '2025-08-20', 'Medication', '2024-11-29'),
('Rhinofex', 'nasal congestion', 140,20, '2025-08-20', 'Medication', '2024-11-29'),
('Otrivin', 'nasal congestion', 140,32, '2025-08-20', 'Medication', '2024-11-29'),
('Candistan', 'treat a variety of fungal infections', 140,14, '2025-08-20', 'Medication', '2024-11-29'),
('Canesten', 'treat a variety of fungal infections', 140,41, '2025-08-20', 'Medication', '2024-11-29'),

-- Cosmetic Products
('LABELLO LIPSTICK', 'Lipstick', 50, 10, '2026-03-15', 'Cosmetic', '2024-11-29'),
('JOKO MATT LIPS LIPSTICK', 'Lipstick', 30, 15, '2026-07-15', 'Cosmetic', '2024-11-29'),
('MUSIC FLOWER ULTRA VELVET MATTE LIPSTICk', 'Lipstick', 80, 15, '2026-07-15', 'Cosmetic', '2024-11-29'),
('YOKO HEALTHY WHITE MOISTURIZER CREAM', 'Hydrating skin moisturizer', 90, 45, '2025-11-20', 'Cosmetic', '2024-11-29'),
('NEUTROGENA HYDRO BOOST GEL CREAM, DRY SKIN', 'Hydrating skin moisturizer', 100, 55, '2025-12-20', 'Cosmetic', '2024-11-29'),
('BIODERM ATODERM GEL CREAM, DRY SKIN', 'Hydrating skin moisturizer', 100, 75, '2026-04-20', 'Cosmetic', '2024-11-29'),
('INSPIRE PERFUMED SPRAY', 'body spray', 30, 25, '2027-08-01', 'Cosmetic', '2024-11-29'),
('MINI CRYSTAL PERFUMED', 'body spray', 20, 25, '2027-09-01', 'Cosmetic', '2024-11-29'),
('MAISON ALHAMBRA EXTRA LONG LASING PERFUMED BODY SPRAY', 'body spray', 40, 25, '2027-08-01', 'Cosmetic', '2024-11-29'),
('BIODERM Sunscreen', 'Sunscreen', 60, 80, '2025-04-15', 'Cosmetic', '2024-11-29'),
('Avene Sunscreen', 'Sunscreen', 60, 110, '2025-08-15', 'Cosmetic', '2024-11-29'),
('Nextgen SPF Sunscreen', 'Sunscreen', 60, 90, '2025-07-15', 'Cosmetic', '2024-11-29'),
('TOPFACE Foundation', 'Foundation', 40, 35, '2026-09-30', 'Cosmetic', '2024-11-29'),
('TONY MAKE UP FOR YOU HD PROFESSIONAL FOUNDATION', 'Foundation', 30, 50, '2026-09-30', 'Cosmetic', '2024-11-29'),
('OSHEA Foundation', 'Foundation', 30, 55, '2026-09-30', 'Cosmetic', '2024-11-29'),
('BIODERM Face Wash', 'Face Wash', 100, 110, '2025-06-05', 'Cosmetic', '2024-11-29'),
('Avene Face Wash', 'Face Wash', 100, 80, '2025-06-05', 'Cosmetic', '2024-11-29'),
('NIVEA CLEANSE & CARE FACE WASH', 'Face Wash', 100, 70, '2025-06-05', 'Cosmetic', '2024-11-29'),
('CHI ROYAL SHAMPOO', 'shampoo', 120, 100, '2026-01-20', 'Cosmetic', '2024-11-29'),
('ALASEEL COSMETICS HAIR SHAMPOO', 'shampoo', 80, 90, '2026-01-20', 'Cosmetic', '2024-11-29'),
('BABY SEBAMED SHAMPOO', 'shampoo', 120, 100, '2026-12-20', 'Cosmetic', '2024-11-29'),
('LANA LINE HELLO BEAUTIFUL HAND CREAM', 'hand cream', 80, 150, '2026-03-10', 'Cosmetic', '2024-11-29'),
('LOVINA CARE TREAT HAND CREAM', 'hand cream', 80, 35, '2026-03-10', 'Cosmetic', '2024-11-29'),
('ESFOLIO FRESH PINK PEACH HAND CREAM', 'hand cream', 80, 70, '2026-03-10', 'Cosmetic', '2024-11-29'),
('TO-ME JOJOBA EXTRACT BODY LOTION', 'body lotion', 90,110, '2025-11-15', 'Cosmetic', '2024-11-29'),
('NIVEA NATURAL GLOW C&A VITAMIN BODY LOTION', 'body lotion', 90,75, '2025-11-15', 'Cosmetic', '2024-11-29'),
('VASU SHEA BUTTER CARE BODY LOTION', 'body lotion', 90,130, '2025-11-15', 'Cosmetic', '2024-11-29'),

('Vitamin D3', 'Vitamin', 100, 36, '2026-02-01', 'Medication', '2024-11-29'),
('Vitamin B12', 'Vitamin', 90, 28, '2028-02-01', 'Medication', '2024-11-29'),
('Vitamin C', 'Vitamin', 70, 41, '2026-12-01', 'Medication', '2024-11-29'),
('VATIKA ONION ENRICHED HAIR OIL', 'Hair Oil', 60, 35, '2026-06-15', 'Cosmetic', '2024-11-29'),
('KISS BEAUTY HAIR OIL', 'Hair Oil', 60, 25, '2026-10-15', 'Cosmetic', '2024-11-29'),
('PURE HAIR OIL', 'Hair Oil', 60, 100, '2026-06-15', 'Cosmetic', '2024-11-29'),
('ULTRA MAX', 'Deodorant', 140, 20, '2026-05-25', 'Cosmetic', '2024-11-29'),
('DOVE', 'Deodorant', 140, 18, '2025-05-25', 'Cosmetic', '2024-11-29'),
('HUGO Deodorant', 'Deodorant', 140, 45, '2028-05-25', 'Cosmetic', '2024-11-29'),
('SUN GEL LOLO PLUS HAND SANITIZER', 'Hand Sanitizer', 50, 30, '2025-03-01', 'Cosmetic', '2024-11-29'),
('HIGEEN ANTI-BACTERIAL HAND SANITIZER', 'Hand Sanitizer', 100, 10, '2027-03-01', 'Cosmetic', '2024-11-29'),
('MIX HAND SANITIZER GEL', 'Hand Sanitizer', 200, 15, '2025-03-01', 'Cosmetic', '2024-11-29'),
('ORAL-B PRO-EXPERT DEEP CLEAN TOOTHPASTE', 'Toothpaste', 90, 15, '2026-07-05', 'Cosmetic', '2024-11-29'),
('SIGNAL COMPLETE Toothpaste', 'Toothpaste', 60, 14, '2026-07-05', 'Cosmetic', '2024-11-29'),
('WHITE GLO PROFESSIONAL CHOICE TOOTHPASTE', 'Toothpaste', 80, 27, '2026-07-05', 'Cosmetic', '2024-11-29');

INSERT INTO CustomerPurchase (CustomerID, ProductID, PurchaseDate)
VALUES
(5, 4, '2024-01-15'),
(5, 7, '2024-01-16'),
(2, 9, '2024-01-20'),
(2, 48, '2024-01-25'),
(3, 70, '2024-02-05'),
(3, 50, '2024-02-10'),
(4, 3, '2024-02-15'),
(5, 67, '2024-02-20'),
(6, 45, '2024-02-22'),
(7, 55, '2024-02-25');

INSERT INTO Pharmacist (Name, ContactInfo, Role, Username, Password, Wage)
VALUES
('Areej Shrateh', '0598567165', 'Senior Pharmacist', 'ashrateh', 'Areej456', '3000.00'),
('Asem Rimawi', '0598567166', 'Senior Pharmacist', 'arimawi', 'Asem456', '2800.00'),
('Sarah Hassan', '0598123456', 'Pharmacist', 'shassan', 'Sarah123', '2500.00'),
('Ahmad Nasser', '0598234567', 'Pharmacist', 'dnasser', 'Ahmad456', '2700.00'),
('Rania Al-Jamal', '0598345678', 'Pharmacist', 'rjamal', 'Rania123', '2600.00');

select * from product;
INSERT INTO Sales (Date, PaymentMethod, Quantity,CustomerID, PharmacistID,productID)
VALUES
('2024-12-29', 'Cash',1,5,2,55),  
('2024-12-29','Card', 2, 2,1,7),  
('2024-12-28','Cash', 3, 3,1,2),   
('2024-12-28','Card', 2, 4,2,32),   
('2024-12-26','Cash', 5, 5,3,38),   
('2024-12-26','Cash', 1, 6,2,40),  
('2024-12-27','Card', 3, 2,5,64),  
('2024-12-27','Card', 3, 3,4,9),   
('2024-12-27','Cash', 2, 4,4,17),  
('2024-12-27','Card', 2, 5,3,4); 

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

INSERT INTO Orders (PharmacistID, ProductID, OrderDate, Quantity)
VALUES
(1, 1, '2024-12-26', 50);

INSERT INTO Orders (PharmacistID, ProductID, OrderDate, Quantity)
VALUES
(1, 7, '2024-12-26', 2);

INSERT INTO Orders (PharmacistID, ProductID, OrderDate, Quantity)
VALUES
(1, 7, '2024-12-27', 9);

select * from Customer;
select * from product;
select * from CustomerPurchase;
select * from Pharmacist;
select * from Orders;
select * from Sales;
