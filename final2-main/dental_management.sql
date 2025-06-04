-- Dental Management System Database Schema
-- MySQL Database Creation Script

-- Create the database
CREATE DATABASE IF NOT EXISTS dental_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE dental_management;

-- Staff table (Users with login capabilities)
CREATE TABLE staff (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'Staff',
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Patients table
CREATE TABLE patient (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(120),
    address TEXT,
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(20),
    medical_history TEXT,
    dental_history TEXT,
    allergies TEXT,
    insurance_provider VARCHAR(100),
    insurance_policy VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Appointments table
CREATE TABLE appointment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    staff_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    duration INT NOT NULL DEFAULT 30,
    appointment_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'Scheduled',
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patient(id) ON DELETE CASCADE,
    FOREIGN KEY (staff_id) REFERENCES staff(id) ON DELETE CASCADE
);

-- Treatments table
CREATE TABLE treatment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    staff_id INT NOT NULL,
    appointment_id INT,
    treatment_date DATE NOT NULL,
    procedure_name VARCHAR(200) NOT NULL,
    tooth_number VARCHAR(10),
    diagnosis TEXT,
    treatment_notes TEXT,
    cost DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'Planned',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patient(id) ON DELETE CASCADE,
    FOREIGN KEY (staff_id) REFERENCES staff(id) ON DELETE CASCADE,
    FOREIGN KEY (appointment_id) REFERENCES appointment(id) ON DELETE SET NULL
);

-- Bills table
CREATE TABLE bill (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    bill_date DATE NOT NULL DEFAULT (CURDATE()),
    due_date DATE NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    paid_amount DECIMAL(10, 2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'Pending',
    payment_method VARCHAR(50),
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patient(id) ON DELETE CASCADE
);

-- Bill Items table
CREATE TABLE bill_item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bill_id INT NOT NULL,
    description VARCHAR(200) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (bill_id) REFERENCES bill(id) ON DELETE CASCADE
);

-- Inventory Items table
CREATE TABLE inventory_item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    current_stock INT NOT NULL DEFAULT 0,
    minimum_stock INT NOT NULL DEFAULT 10,
    unit_cost DECIMAL(10, 2),
    supplier VARCHAR(100),
    last_restocked DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Communications table
CREATE TABLE communication (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    type VARCHAR(20) NOT NULL,
    subject VARCHAR(200),
    message TEXT NOT NULL,
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Sent',
    FOREIGN KEY (patient_id) REFERENCES patient(id) ON DELETE CASCADE
);

-- Insert default admin user
INSERT INTO staff (username, email, password_hash, first_name, last_name, role) VALUES 
('admin', 'admin@dentalclinic.com', 'scrypt:32768:8:1$WpgNQpx8IzPeXzU8$2c8b8f9d8e7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1', 'Admin', 'User', 'Administrator');

-- Insert sample patients
INSERT INTO patient (first_name, last_name, date_of_birth, gender, phone, email, address) VALUES 
('John', 'Doe', '1985-03-15', 'Male', '+63-912-345-6789', 'john.doe@email.com', '123 Main St, Manila, Philippines'),
('Maria', 'Santos', '1990-07-22', 'Female', '+63-917-654-3210', 'maria.santos@email.com', '456 Rizal Ave, Quezon City, Philippines'),
('Roberto', 'Cruz', '1978-11-08', 'Male', '+63-920-111-2222', 'roberto.cruz@email.com', '789 EDSA, Makati, Philippines');

-- Insert sample appointments
INSERT INTO appointment (patient_id, staff_id, appointment_date, appointment_time, duration, appointment_type, notes) VALUES 
(1, 1, CURDATE() + INTERVAL 1 DAY, '09:00:00', 60, 'Check-up', 'Regular dental checkup'),
(2, 1, CURDATE() + INTERVAL 2 DAY, '10:30:00', 30, 'Cleaning', 'Teeth cleaning session'),
(3, 1, CURDATE() + INTERVAL 3 DAY, '14:00:00', 90, 'Root Canal', 'Root canal treatment for tooth #18');

-- Insert sample treatments
INSERT INTO treatment (patient_id, staff_id, treatment_date, procedure_name, tooth_number, diagnosis, treatment_notes, cost, status) VALUES 
(1, 1, CURDATE() - INTERVAL 30 DAY, 'Dental Filling', '14', 'Cavity in upper right molar', 'Composite filling applied successfully', 3500.00, 'Completed'),
(2, 1, CURDATE() - INTERVAL 15 DAY, 'Teeth Cleaning', NULL, 'Plaque buildup', 'Professional cleaning completed', 2500.00, 'Completed'),
(3, 1, CURDATE() - INTERVAL 7 DAY, 'Tooth Extraction', '32', 'Severely damaged wisdom tooth', 'Extraction completed without complications', 5000.00, 'Completed');

-- Insert sample bills
INSERT INTO bill (patient_id, due_date, total_amount, paid_amount, status, payment_method, notes) VALUES 
(1, CURDATE() + INTERVAL 30 DAY, 3500.00, 3500.00, 'Paid', 'Cash', 'Payment for dental filling'),
(2, CURDATE() + INTERVAL 15 DAY, 2500.00, 0.00, 'Pending', NULL, 'Payment for teeth cleaning'),
(3, CURDATE() + INTERVAL 7 DAY, 5000.00, 2500.00, 'Partial', 'BDO Bank Transfer', 'Partial payment for tooth extraction');

-- Insert bill items
INSERT INTO bill_item (bill_id, description, quantity, unit_price, total_price) VALUES 
(1, 'Composite Filling', 1, 3500.00, 3500.00),
(2, 'Professional Teeth Cleaning', 1, 2500.00, 2500.00),
(3, 'Wisdom Tooth Extraction', 1, 5000.00, 5000.00);

-- Insert sample inventory items
INSERT INTO inventory_item (name, description, category, current_stock, minimum_stock, unit_cost, supplier) VALUES 
('Dental Composite Resin', 'High-quality composite resin for fillings', 'Materials', 25, 10, 850.00, 'Dental Supply Corp'),
('Disposable Gloves', 'Latex-free disposable examination gloves', 'Supplies', 500, 100, 2.50, 'Medical Supplies Inc'),
('Dental Mirrors', 'Stainless steel dental examination mirrors', 'Instruments', 15, 5, 120.00, 'Dental Tools Ltd'),
('Local Anesthetic', 'Lidocaine 2% with epinephrine', 'Medications', 8, 15, 45.00, 'Pharma Solutions'),
('Dental Burs', 'High-speed carbide dental burs set', 'Instruments', 12, 20, 380.00, 'Precision Dental Tools');