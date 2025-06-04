from datetime import datetime, timedelta, time
from random import choice, randint, sample
from faker import Faker
from app import app, db
from models import Patient, Staff, Appointment, Treatment, Bill, BillItem
import sys
import os

# Add the parent directory to the path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Initialize Faker for generating fake data
fake = Faker()

# Configure the application
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Enable SQL query logging for debugging

def create_dentists():
    """Create or get dentists Joan and Sarah"""
    try:
        # Check if dentists already exist
        joan = Staff.query.filter_by(username='joan').first()
        sarah = Staff.query.filter_by(username='sarah').first()
        
        if not joan:
            joan = Staff(
                username='joan',
                email='joan.dentist@example.com',
                password_hash='hashed_password_123',  # In a real app, use proper password hashing
                first_name='Joan',
                last_name='Smith',
                role='Dentist',
                phone='09171234567',
                is_active=True
            )
            db.session.add(joan)
        
        if not sarah:
            sarah = Staff(
                username='sarah',
                email='sarah.dentist@example.com',
                password_hash='hashed_password_456',  # In a real app, use proper password hashing
                first_name='Sarah',
                last_name='Johnson',
                role='Dentist',
                phone='09172345678',
                is_active=True
            )
            db.session.add(sarah)
        
        db.session.commit()
        return joan, sarah
    except Exception as e:
        db.session.rollback()
        print(f"Error in create_dentists: {str(e)}")
        raise

def create_sample_patients_with_appointments():
    """Create 15 patients with appointments and treatments"""
    # Get or create dentists
    joan, sarah = create_dentists()
    dentists = [joan, sarah]
    
    # Sample data for patients
    first_names = ['Miguel', 'Sofia', 'Gabriel', 'Isabella', 'Diego', 'Valentina', 
                  'Santiago', 'Camila', 'Mateo', 'Valeria', 'Nicolas', 'Mariana',
                  'Alejandro', 'Daniela', 'Javier']
    last_names = ['Santos', 'Reyes', 'Bautista', 'Ocampo', 'Mendoza', 'Aquino',
                 'Villanueva', 'Del Rosario', 'Gonzales', 'Castro', 'Dela Cruz',
                 'Lim', 'Tan', 'Chua', 'Sy']
    
    # Treatment types and their costs
    treatments = [
        ('Dental Check-up', 1000, 30, 'Routine dental examination and cleaning'),
        ('Tooth Filling', 2500, 45, 'Dental filling for cavity'),
        ('Root Canal', 15000, 90, 'Root canal treatment'),
        ('Tooth Extraction', 3000, 30, 'Simple tooth extraction'),
        ('Dental Crown', 12000, 60, 'Porcelain crown placement'),
        ('Teeth Whitening', 8000, 60, 'Professional teeth whitening'),
        ('Dental Implant', 50000, 120, 'Single tooth implant')
    ]
        
    # Create 15 patients with appointments and treatments
    for i in range(15):
        # Create patient
        patient = Patient(
            first_name=first_names[i],
            last_name=last_names[i],
            date_of_birth=fake.date_between(start_date='-60y', end_date='-18y'),
            gender=choice(['Male', 'Female']),
            phone=f'09{randint(10, 99)}{randint(1000000, 9999999)}',
            email=f'{first_names[i].lower()}.{last_names[i].lower()}@example.com',
            address=fake.address(),
            emergency_contact_name=fake.name(),
            emergency_contact_phone=f'09{randint(10, 99)}{randint(1000000, 9999999)}',
            medical_history=choice(['None', 'Hypertension', 'Diabetes', 'Asthma', 'Allergies']),
            dental_history=choice(['Regular check-ups', 'Previous fillings', 'Gum treatment', 'Braces']),
            allergies=choice(['None', 'Penicillin', 'Latex', 'Local Anesthesia']),
            insurance_provider=choice(['Maxicare', 'MediCard', 'PhilHealth', 'Intellicare', None]),
            insurance_policy=f'POL{randint(100000, 999999)}' if randint(0, 3) > 0 else None
        )
        db.session.add(patient)
        db.session.flush()  # Get the patient ID
        
        # Create 1-3 appointments per patient
        num_appointments = randint(1, 3)
        for _ in range(num_appointments):
            # Schedule appointment in the next 30 days
            appointment_date = datetime.now().date() + timedelta(days=randint(1, 30))
            appointment_time = time(hour=randint(9, 16), minute=choice([0, 15, 30, 45]))
            
            # Choose a random treatment
            treatment_type, cost, duration, notes = choice(treatments)
            
            # Create appointment
            appointment = Appointment(
                patient_id=patient.id,
                staff_id=choice(dentists).id,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                duration=duration,
                appointment_type=treatment_type,
                status=choice(['Scheduled', 'Scheduled', 'Scheduled', 'Completed']),
                notes=f"Patient reported {choice(['no issues', 'mild pain', 'sensitivity'])}. {notes}"
            )
            db.session.add(appointment)
            db.session.flush()  # Get the appointment ID
            
            # Create treatment record
            treatment = Treatment(
                patient_id=patient.id,
                staff_id=appointment.staff_id,
                appointment_id=appointment.id,
                treatment_date=appointment_date,
                procedure_name=treatment_type,
                tooth_number=f"{randint(1, 32)}" if randint(0, 1) else None,
                diagnosis=f"Diagnosis for {treatment_type}",
                treatment_notes=f"Performed {treatment_type}. {notes}",
                cost=cost,
                status='Completed' if appointment.status == 'Completed' else 'Planned'
            )
            db.session.add(treatment)
            
            # Create bill for completed treatments
            if appointment.status == 'Completed':
                bill = Bill(
                    patient_id=patient.id,
                    bill_date=appointment_date,
                    due_date=appointment_date + timedelta(days=30),
                    total_amount=cost,
                    paid_amount=cost if randint(0, 1) else cost * 0.5,
                    status='Paid' if randint(0, 1) else 'Pending',
                    payment_method=choice(['Cash', 'BDO Bank Transfer', 'GCash']),
                    notes=f"Payment for {treatment_type}"
                )
                db.session.add(bill)
                db.session.flush()
                
                # Add bill item
                bill_item = BillItem(
                    bill_id=bill.id,
                    description=treatment_type,
                    quantity=1,
                    unit_price=cost,
                    total_price=cost
                )
                db.session.add(bill_item)
    
    try:
        db.session.commit()
        print("Successfully added 15 patients with appointments and treatments.")
        
        # Print summary
        print(f"\nAdded patients:")
        patients = Patient.query.order_by(Patient.id.desc()).limit(15).all()
        for p in patients:
            print(f"- {p.first_name} {p.last_name} (ID: {p.id})")
            
        print(f"\nDentists:")
        print(f"- Dr. {joan.first_name} {joan.last_name} (ID: {joan.id})")
        print(f"- Dr. {sarah.first_name} {sarah.last_name} (ID: {sarah.id})")
        
        print("\nAppointments and treatments have been scheduled.")
        
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    print("Starting to add sample patients with appointments...")
    with app.app_context():
        try:
            # Create all database tables if they don't exist
            print("Creating database tables if they don't exist...")
            db.create_all()
            print("Database tables created/verified.")
            
            print("Starting to create sample data...")
            create_sample_patients_with_appointments()
            print("Sample data creation completed successfully!")
        except Exception as e:
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
