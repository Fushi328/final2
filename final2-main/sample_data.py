from app import app, db
from models import Patient, InventoryItem
from datetime import datetime, date
from werkzeug.security import generate_password_hash

def create_sample_data():
    with app.app_context():
        # Sample patients
        patients = [
            {
                'first_name': 'John', 'last_name': 'Doe', 'date_of_birth': date(1985, 5, 15),
                'gender': 'Male', 'address': '123 Main St', 'phone': '555-0101',
                'email': 'john.doe@example.com', 'insurance_provider': 'Blue Cross',
                'insurance_number': 'BC12345678', 'medical_history': 'None', 'allergies': 'None'
            },
            {
                'first_name': 'Jane', 'last_name': 'Smith', 'date_of_birth': date(1990, 8, 22),
                'gender': 'Female', 'address': '456 Oak Ave', 'phone': '555-0102',
                'email': 'jane.smith@example.com', 'insurance_provider': 'Aetna',
                'insurance_number': 'AE98765432', 'medical_history': 'Asthma', 'allergies': 'Penicillin'
            },
            {
                'first_name': 'Robert', 'last_name': 'Johnson', 'date_of_birth': date(1978, 3, 10),
                'gender': 'Male', 'address': '789 Pine Rd', 'phone': '555-0103',
                'email': 'robert.j@example.com', 'insurance_provider': 'Cigna',
                'insurance_number': 'CI45678901', 'medical_history': 'Diabetes', 'allergies': 'Latex'
            },
            {
                'first_name': 'Emily', 'last_name': 'Williams', 'date_of_birth': date(1995, 11, 30),
                'gender': 'Female', 'address': '321 Elm St', 'phone': '555-0104',
                'email': 'emily.w@example.com', 'insurance_provider': 'United Health',
                'insurance_number': 'UH23456789', 'medical_history': 'None', 'allergies': 'None'
            },
            {
                'first_name': 'Michael', 'last_name': 'Brown', 'date_of_birth': date(1982, 7, 14),
                'gender': 'Male', 'address': '654 Maple Dr', 'phone': '555-0105',
                'email': 'michael.b@example.com', 'insurance_provider': 'Humana',
                'insurance_number': 'HU34567890', 'medical_history': 'Hypertension', 'allergies': 'Aspirin'
            },
            {
                'first_name': 'Sarah', 'last_name': 'Davis', 'date_of_birth': date(1989, 4, 5),
                'gender': 'Female', 'address': '987 Cedar Ln', 'phone': '555-0106',
                'email': 'sarah.d@example.com', 'insurance_provider': 'Kaiser',
                'insurance_number': 'KA45678901', 'medical_history': 'Anxiety', 'allergies': 'Codeine'
            },
            {
                'first_name': 'David', 'last_name': 'Miller', 'date_of_birth': date(1975, 9, 18),
                'gender': 'Male', 'address': '159 Birch St', 'phone': '555-0107',
                'email': 'david.m@example.com', 'insurance_provider': 'Blue Shield',
                'insurance_number': 'BS56789012', 'medical_history': 'High Cholesterol', 'allergies': 'None'
            },
            {
                'first_name': 'Jennifer', 'last_name': 'Wilson', 'date_of_birth': date(1992, 12, 22),
                'gender': 'Female', 'address': '753 Willow Way', 'phone': '555-0108',
                'email': 'jennifer.w@example.com', 'insurance_provider': 'Aetna',
                'insurance_number': 'AE67890123', 'medical_history': 'None', 'allergies': 'Sulfa'
            },
            {
                'first_name': 'James', 'last_name': 'Taylor', 'date_of_birth': date(1980, 6, 8),
                'gender': 'Male', 'address': '246 Spruce Ave', 'phone': '555-0109',
                'email': 'james.t@example.com', 'insurance_provider': 'Cigna',
                'insurance_number': 'CI78901234', 'medical_history': 'Sleep Apnea', 'allergies': 'Latex'
            },
            {
                'first_name': 'Lisa', 'last_name': 'Anderson', 'date_of_birth': date(1987, 2, 14),
                'gender': 'Female', 'address': '864 Redwood Blvd', 'phone': '555-0110',
                'email': 'lisa.a@example.com', 'insurance_provider': 'Blue Cross',
                'insurance_number': 'BC89012345', 'medical_history': 'Migraine', 'allergies': 'None'
            },
            {
                'first_name': 'Christopher', 'last_name': 'Thomas', 'date_of_birth': date(1972, 10, 31),
                'gender': 'Male', 'address': '975 Sequoia Dr', 'phone': '555-0111',
                'email': 'chris.t@example.com', 'insurance_provider': 'United Health',
                'insurance_number': 'UH90123456', 'medical_history': 'Heart Disease', 'allergies': 'Penicillin'
            },
            {
                'first_name': 'Jessica', 'last_name': 'Jackson', 'date_of_birth': date(1993, 7, 3),
                'gender': 'Female', 'address': '135 Magnolia Ln', 'phone': '555-0112',
                'email': 'jessica.j@example.com', 'insurance_provider': 'Humana',
                'insurance_number': 'HU01234567', 'medical_history': 'Anemia', 'allergies': 'Iodine'
            },
            {
                'first_name': 'Daniel', 'last_name': 'White', 'date_of_birth': date(1984, 1, 25),
                'gender': 'Male', 'address': '864 Dogwood Dr', 'phone': '555-0113',
                'email': 'daniel.w@example.com', 'insurance_provider': 'Kaiser',
                'insurance_number': 'KA12345678', 'medical_history': 'None', 'allergies': 'None'
            },
            {
                'first_name': 'Amanda', 'last_name': 'Harris', 'date_of_birth': date(1991, 9, 17),
                'gender': 'Female', 'address': '975 Cypress Ct', 'phone': '555-0114',
                'email': 'amanda.h@example.com', 'insurance_provider': 'Blue Shield',
                'insurance_number': 'BS23456789', 'medical_history': 'Asthma', 'allergies': 'Aspirin'
            },
            {
                'first_name': 'Matthew', 'last_name': 'Martin', 'date_of_birth': date(1979, 11, 8),
                'gender': 'Male', 'address': '741 Juniper Way', 'phone': '555-0115',
                'email': 'matthew.m@example.com', 'insurance_provider': 'Aetna',
                'insurance_number': 'AE34567890', 'medical_history': 'Diabetes', 'allergies': 'Sulfa'
            },
            {
                'first_name': 'Ashley', 'last_name': 'Thompson', 'date_of_birth': date(1986, 4, 19),
                'gender': 'Female', 'address': '852 Redbud Ln', 'phone': '555-0116',
                'email': 'ashley.t@example.com', 'insurance_provider': 'Cigna',
                'insurance_number': 'CI45678901', 'medical_history': 'None', 'allergies': 'Latex'
            },
            {
                'first_name': 'Andrew', 'last_name': 'Garcia', 'date_of_birth': date(1976, 8, 12),
                'gender': 'Male', 'address': '963 Sycamore St', 'phone': '555-0117',
                'email': 'andrew.g@example.com', 'insurance_provider': 'Blue Cross',
                'insurance_number': 'BC56789012', 'medical_history': 'High Blood Pressure', 'allergies': 'None'
            },
            {
                'first_name': 'Stephanie', 'last_name': 'Martinez', 'date_of_birth': date(1994, 2, 27),
                'gender': 'Female', 'address': '159 Mulberry Dr', 'phone': '555-0118',
                'email': 'steph.m@example.com', 'insurance_provider': 'United Health',
                'insurance_number': 'UH67890123', 'medical_history': 'Anxiety', 'allergies': 'Penicillin'
            },
            {
                'first_name': 'Ryan', 'last_name': 'Robinson', 'date_of_birth': date(1983, 6, 9),
                'gender': 'Male', 'address': '753 Poplar Ave', 'phone': '555-0119',
                'email': 'ryan.r@example.com',
                'insurance_provider': 'Humana',
                'insurance_number': 'HU78901234', 'medical_history': 'None', 'allergies': 'Iodine'
            },
            {
                'first_name': 'Lauren', 'last_name': 'Clark', 'date_of_birth': date(1990, 12, 3),
                'gender': 'Female', 'address': '357 Willow Way', 'phone': '555-0120',
                'email': 'lauren.c@example.com',
                'insurance_provider': 'Kaiser',
                'insurance_number': 'KA89012345', 'medical_history': 'Migraine', 'allergies': 'None'
            }
        ]

        # Sample inventory items
        inventory_items = [
            {'name': 'Dental Floss (50m)', 'description': 'Waxed dental floss', 'quantity': 100, 'unit': 'rolls', 'unit_price': 2.50, 'supplier': 'Oral-B', 'reorder_level': 20},
            {'name': 'Toothbrush (Soft)', 'description': 'Soft-bristle toothbrush', 'quantity': 150, 'unit': 'pieces', 'unit_price': 1.75, 'supplier': 'Colgate', 'reorder_level': 30},
            {'name': 'Toothpaste (100g)', 'description': 'Fluoride toothpaste', 'quantity': 80, 'unit': 'tubes', 'unit_price': 3.25, 'supplier': 'Crest', 'reorder_level': 25},
            {'name': 'Mouthwash (500ml)', 'description': 'Antiseptic mouthwash', 'quantity': 60, 'unit': 'bottles', 'unit_price': 4.50, 'supplier': 'Listerine', 'reorder_level': 15},
            {'name': 'Dental Bibs (100pcs)', 'description': 'Disposable dental bibs', 'quantity': 200, 'unit': 'packs', 'unit_price': 8.99, 'supplier': 'DentalEZ', 'reorder_level': 40},
            {'name': 'Examination Gloves (100pcs)', 'description': 'Latex-free gloves', 'quantity': 50, 'unit': 'boxes', 'unit_price': 12.99, 'supplier': 'MedPride', 'reorder_level': 20},
            {'name': 'Face Masks (50pcs)', 'description': '3-ply surgical masks', 'quantity': 30, 'unit': 'boxes', 'unit_price': 15.99, 'supplier': '3M', 'reorder_level': 10},
            {'name': 'Dental Anesthetic (50mg)', 'description': 'Lidocaine HCL 2%', 'quantity': 40, 'unit': 'vials', 'unit_price': 5.75, 'supplier': 'Septodont', 'reorder_level': 15},
            {'name': 'Saliva Ejectors (100pcs)', 'description': 'Disposable saliva ejectors', 'quantity': 120, 'unit': 'packs', 'unit_price': 7.25, 'supplier': 'Dentsply', 'reorder_level': 30},
            {'name': 'Prophy Cups (100pcs)', 'description': 'Rubber prophy cups', 'quantity': 90, 'unit': 'packs', 'unit_price': 18.50, 'supplier': 'Kerr', 'reorder_level': 25},
            {'name': 'X-Ray Films (100pcs)', 'description': 'Dental X-ray films', 'quantity': 25, 'unit': 'boxes', 'unit_price': 45.99, 'supplier': 'Kodak', 'reorder_level': 8},
            {'name': 'Cotton Rolls (1000pcs)', 'description': 'Sterile cotton rolls', 'quantity': 15, 'unit': 'bags', 'unit_price': 22.99, 'supplier': 'GAC', 'reorder_level': 5},
            {'name': 'Disposable Mirrors (50pcs)', 'description': 'Single-use dental mirrors', 'quantity': 70, 'unit': 'packs', 'unit_price': 14.99, 'supplier': 'Hu-Friedy', 'reorder_level': 20},
            {'name': 'Bone Graft Material (0.5g)', 'description': 'Synthetic bone graft', 'quantity': 35, 'unit': 'vials', 'unit_price': 65.00, 'supplier': 'BioHorizons', 'reorder_level': 10},
            {'name': 'Suture Material (4-0)', 'description': 'Absorbable sutures', 'quantity': 40, 'unit': 'packs', 'unit_price': 28.50, 'supplier': 'Ethicon', 'reorder_level': 12}
        ]

        print("Adding sample patients...")
        for patient_data in patients:
            patient = Patient(**patient_data)
            db.session.add(patient)
        
        print("Adding sample inventory items...")
        for item_data in inventory_items:
            item = InventoryItem(**item_data)
            db.session.add(item)
        
        db.session.commit()
        print("Sample data added successfully!")
        print(f"Added {len(patients)} patients and {len(inventory_items)} inventory items.")

if __name__ == '__main__':
    create_sample_data()
