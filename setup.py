#!/usr/bin/env python3
"""
Setup script for Dental Management System
This script initializes the database and creates sample data
"""

import os
import sys
from datetime import date, timedelta
from decimal import Decimal

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Staff, Patient, Appointment, Treatment, Bill, BillItem, InventoryItem, Communication
from werkzeug.security import generate_password_hash

def create_sample_data():
    """Create comprehensive sample data for the dental management system"""
    print("Creating sample data...")
    
    # Create admin staff
    admin = Staff(
        username='admin',
        email='admin@dental.com',
        password_hash=generate_password_hash('admin123'),
        first_name='Admin',
        last_name='User',
        role='Admin',
        phone='555-0001',
        is_active=True
    )
    db.session.add(admin)
    
    # Create sample patients
    patients_data = [
        ('John', 'Doe', '1985-03-15', 'Male', '555-1001', 'john.doe@email.com'),
        ('Jane', 'Smith', '1990-07-22', 'Female', '555-1002', 'jane.smith@email.com'),
        ('Mike', 'Johnson', '1978-11-08', 'Male', '555-1003', 'mike.johnson@email.com'),
        ('Sarah', 'Brown', '1992-05-12', 'Female', '555-1004', 'sarah.brown@email.com'),
        ('David', 'Wilson', '1988-09-30', 'Male', '555-1005', 'david.wilson@email.com')
    ]
    
    patients = []
    for fname, lname, dob, gender, phone, email in patients_data:
        patient = Patient(
            first_name=fname,
            last_name=lname,
            date_of_birth=datetime.strptime(dob, '%Y-%m-%d').date(),
            gender=gender,
            phone=phone,
            email=email,
            address=f"123 Main St, City, State",
            medical_history="No known allergies",
            dental_history="Regular checkups"
        )
        patients.append(patient)
        db.session.add(patient)
    
    db.session.flush()  # Get patient IDs
    
    # Create today's appointments for real-time demo
    from datetime import time
    appointment_times = [
        time(9, 0), time(10, 30), time(11, 0), time(14, 0), 
        time(15, 30), time(16, 0)
    ]
    
    for i, apt_time in enumerate(appointment_times):
        if i < len(patients):
            appointment = Appointment(
                patient_id=patients[i].id,
                staff_id=admin.id,
                appointment_date=date.today(),
                appointment_time=apt_time,
                duration=30,
                appointment_type='Checkup',
                status='Scheduled'
            )
            db.session.add(appointment)
    
    # Create sample inventory items
    inventory_items = [
        ('Dental Gloves', 'Disposable latex gloves', 'Consumables', 25, 100, 0.50),
        ('Anesthesia', 'Local anesthetic cartridges', 'Medications', 80, 50, 15.00),
        ('X-ray Films', 'Digital x-ray films', 'Equipment', 10, 100, 5.00),
        ('Dental Floss', 'Patient education floss', 'Hygiene', 150, 50, 2.00),
        ('Fluoride', 'Fluoride treatment gel', 'Treatment', 45, 20, 25.00)
    ]
    
    for name, desc, category, stock, min_stock, cost in inventory_items:
        item = InventoryItem(
            name=name,
            description=desc,
            category=category,
            current_stock=stock,
            minimum_stock=min_stock,
            unit_cost=Decimal(str(cost)),
            supplier='Dental Supply Co.',
            last_restocked=date.today() - timedelta(days=30)
        )
        db.session.add(item)
    
    # Create sample treatments
    treatment = Treatment(
        patient_id=patients[0].id,
        staff_id=admin.id,
        treatment_date=date.today(),
        procedure_name='Dental Cleaning',
        diagnosis='Routine cleaning',
        treatment_notes='Standard cleaning procedure completed',
        cost=Decimal('2500.00'),
        status='Completed'
    )
    db.session.add(treatment)
    
    # Create sample bill
    bill = Bill(
        patient_id=patients[0].id,
        bill_date=date.today(),
        due_date=date.today() + timedelta(days=30),
        total_amount=Decimal('2500.00'),
        paid_amount=Decimal('0.00'),
        status='Pending',
        payment_method='Cash'
    )
    db.session.add(bill)
    db.session.flush()
    
    # Add bill item
    bill_item = BillItem(
        bill_id=bill.id,
        description='Dental Cleaning',
        quantity=1,
        unit_price=Decimal('2500.00'),
        total_price=Decimal('2500.00')
    )
    db.session.add(bill_item)
    
    db.session.commit()
    print("Sample data created successfully!")

if __name__ == '__main__':
    with app.app_context():
        print("Initializing Dental Management System Database...")
        
        # Create all tables
        db.create_all()
        print("Database tables created.")
        
        # Check if admin user already exists
        if not Staff.query.filter_by(username='admin').first():
            create_sample_data()
        else:
            print("Sample data already exists.")
        
        print("Setup complete!")
        print("\nLogin credentials:")
        print("Username: admin")
        print("Password: admin123")

def create_sample_data():
    """Create sample data for demonstration"""
    
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        print("Creating sample data...")
        
        # Create default admin user
        admin_user = Staff(
            username='admin',
            email='admin@dentalclinic.com',
            first_name='Admin',
            last_name='User',
            role='Administrator',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin_user)
        
        # Create additional staff
        dentist = Staff(
            username='dr.smith',
            email='dr.smith@dentalclinic.com',
            first_name='Sarah',
            last_name='Smith',
            role='Dentist',
            password_hash=generate_password_hash('password123')
        )
        db.session.add(dentist)
        
        # Create sample patients
        patients_data = [
            {
                'first_name': 'Juan',
                'last_name': 'dela Cruz',
                'date_of_birth': date(1985, 3, 15),
                'gender': 'Male',
                'phone': '+63-912-345-6789',
                'email': 'juan.delacruz@email.com',
                'address': '123 Main St, Manila, Philippines'
            },
            {
                'first_name': 'Maria',
                'last_name': 'Santos',
                'date_of_birth': date(1990, 7, 22),
                'gender': 'Female',
                'phone': '+63-917-654-3210',
                'email': 'maria.santos@email.com',
                'address': '456 Rizal Ave, Quezon City, Philippines'
            },
            {
                'first_name': 'Roberto',
                'last_name': 'Cruz',
                'date_of_birth': date(1978, 11, 8),
                'gender': 'Male',
                'phone': '+63-920-111-2222',
                'email': 'roberto.cruz@email.com',
                'address': '789 EDSA, Makati, Philippines'
            }
        ]
        
        patients = []
        for patient_data in patients_data:
            patient = Patient(**patient_data)
            db.session.add(patient)
            patients.append(patient)
        
        db.session.commit()  # Commit to get patient IDs
        
        # Create sample appointments
        appointments_data = [
            {
                'patient_id': patients[0].id,
                'staff_id': admin_user.id,
                'appointment_date': date.today() + timedelta(days=1),
                'appointment_time': '09:00',
                'duration': 60,
                'appointment_type': 'Check-up',
                'notes': 'Regular dental checkup'
            },
            {
                'patient_id': patients[1].id,
                'staff_id': admin_user.id,
                'appointment_date': date.today() + timedelta(days=2),
                'appointment_time': '10:30',
                'duration': 30,
                'appointment_type': 'Cleaning',
                'notes': 'Teeth cleaning session'
            },
            {
                'patient_id': patients[2].id,
                'staff_id': admin_user.id,
                'appointment_date': date.today() + timedelta(days=3),
                'appointment_time': '14:00',
                'duration': 90,
                'appointment_type': 'Root Canal',
                'notes': 'Root canal treatment for tooth #18'
            }
        ]
        
        for appointment_data in appointments_data:
            appointment = Appointment(**appointment_data)
            db.session.add(appointment)
        
        # Create sample treatments
        treatments_data = [
            {
                'patient_id': patients[0].id,
                'staff_id': admin_user.id,
                'treatment_date': date.today() - timedelta(days=30),
                'procedure_name': 'Dental Filling',
                'tooth_number': '14',
                'diagnosis': 'Cavity in upper right molar',
                'treatment_notes': 'Composite filling applied successfully',
                'cost': Decimal('3500.00'),
                'status': 'Completed'
            },
            {
                'patient_id': patients[1].id,
                'staff_id': admin_user.id,
                'treatment_date': date.today() - timedelta(days=15),
                'procedure_name': 'Teeth Cleaning',
                'diagnosis': 'Plaque buildup',
                'treatment_notes': 'Professional cleaning completed',
                'cost': Decimal('2500.00'),
                'status': 'Completed'
            },
            {
                'patient_id': patients[2].id,
                'staff_id': admin_user.id,
                'treatment_date': date.today() - timedelta(days=7),
                'procedure_name': 'Tooth Extraction',
                'tooth_number': '32',
                'diagnosis': 'Severely damaged wisdom tooth',
                'treatment_notes': 'Extraction completed without complications',
                'cost': Decimal('5000.00'),
                'status': 'Completed'
            }
        ]
        
        for treatment_data in treatments_data:
            treatment = Treatment(**treatment_data)
            db.session.add(treatment)
        
        # Create sample bills
        bills_data = [
            {
                'patient_id': patients[0].id,
                'due_date': date.today() + timedelta(days=30),
                'total_amount': Decimal('3500.00'),
                'paid_amount': Decimal('3500.00'),
                'status': 'Paid',
                'payment_method': 'Cash',
                'notes': 'Payment for dental filling'
            },
            {
                'patient_id': patients[1].id,
                'due_date': date.today() + timedelta(days=15),
                'total_amount': Decimal('2500.00'),
                'paid_amount': Decimal('0.00'),
                'status': 'Pending',
                'notes': 'Payment for teeth cleaning'
            },
            {
                'patient_id': patients[2].id,
                'due_date': date.today() + timedelta(days=7),
                'total_amount': Decimal('5000.00'),
                'paid_amount': Decimal('2500.00'),
                'status': 'Partial',
                'payment_method': 'BDO Bank Transfer',
                'notes': 'Partial payment for tooth extraction'
            }
        ]
        
        bills = []
        for bill_data in bills_data:
            bill = Bill(**bill_data)
            db.session.add(bill)
            bills.append(bill)
        
        db.session.commit()  # Commit to get bill IDs
        
        # Create bill items
        bill_items_data = [
            {
                'bill_id': bills[0].id,
                'description': 'Composite Filling',
                'quantity': 1,
                'unit_price': Decimal('3500.00'),
                'total_price': Decimal('3500.00')
            },
            {
                'bill_id': bills[1].id,
                'description': 'Professional Teeth Cleaning',
                'quantity': 1,
                'unit_price': Decimal('2500.00'),
                'total_price': Decimal('2500.00')
            },
            {
                'bill_id': bills[2].id,
                'description': 'Wisdom Tooth Extraction',
                'quantity': 1,
                'unit_price': Decimal('5000.00'),
                'total_price': Decimal('5000.00')
            }
        ]
        
        for item_data in bill_items_data:
            item = BillItem(**item_data)
            db.session.add(item)
        
        # Create sample inventory items
        inventory_data = [
            {
                'name': 'Dental Composite Resin',
                'description': 'High-quality composite resin for fillings',
                'category': 'Materials',
                'current_stock': 25,
                'minimum_stock': 10,
                'unit_cost': Decimal('850.00'),
                'supplier': 'Dental Supply Corp'
            },
            {
                'name': 'Disposable Gloves',
                'description': 'Latex-free disposable examination gloves',
                'category': 'Supplies',
                'current_stock': 500,
                'minimum_stock': 100,
                'unit_cost': Decimal('2.50'),
                'supplier': 'Medical Supplies Inc'
            },
            {
                'name': 'Dental Mirrors',
                'description': 'Stainless steel dental examination mirrors',
                'category': 'Instruments',
                'current_stock': 15,
                'minimum_stock': 5,
                'unit_cost': Decimal('120.00'),
                'supplier': 'Dental Tools Ltd'
            },
            {
                'name': 'Local Anesthetic',
                'description': 'Lidocaine 2% with epinephrine',
                'category': 'Medications',
                'current_stock': 8,
                'minimum_stock': 15,
                'unit_cost': Decimal('45.00'),
                'supplier': 'Pharma Solutions'
            },
            {
                'name': 'Dental Burs',
                'description': 'High-speed carbide dental burs set',
                'category': 'Instruments',
                'current_stock': 12,
                'minimum_stock': 20,
                'unit_cost': Decimal('380.00'),
                'supplier': 'Precision Dental Tools'
            }
        ]
        
        for inventory_item_data in inventory_data:
            item = InventoryItem(**inventory_item_data)
            db.session.add(item)
        
        db.session.commit()
        print("Sample data created successfully!")
        print("\nLogin credentials:")
        print("Username: admin")
        print("Password: admin123")

if __name__ == '__main__':
    create_sample_data()