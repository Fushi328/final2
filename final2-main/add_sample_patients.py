from datetime import datetime, timedelta
from random import choice, randint, sample
import random
from faker import Faker
from app import app, db
from models import Patient, Staff, Appointment, Treatment, Bill, BillItem

# Initialize Faker for generating fake data
fake = Faker()

def create_sample_patients():
    # Sample data for patients
    patients_data = [
        {'first_name': 'Juan', 'last_name': 'Dela Cruz', 'date_of_birth': '1985-06-15', 'gender': 'Male', 'phone': '09171234567', 'email': 'juan.delacruz@example.com'},
        {'first_name': 'Maria', 'last_name': 'Santos', 'date_of_birth': '1990-03-22', 'gender': 'Female', 'phone': '09172345678', 'email': 'maria.santos@example.com'},
        {'first_name': 'Jose', 'last_name': 'Reyes', 'date_of_birth': '1978-11-05', 'gender': 'Male', 'phone': '09173456789', 'email': 'jose.reyes@example.com'},
        {'first_name': 'Ana', 'last_name': 'Gonzales', 'date_of_birth': '1995-08-30', 'gender': 'Female', 'phone': '09174567890', 'email': 'ana.gonzales@example.com'},
        {'first_name': 'Pedro', 'last_name': 'Bautista', 'date_of_birth': '1982-04-18', 'gender': 'Male', 'phone': '09175678901', 'email': 'pedro.bautista@example.com'},
        {'first_name': 'Luz', 'last_name': 'Villanueva', 'date_of_birth': '1975-12-10', 'gender': 'Female', 'phone': '09176789012', 'email': 'luz.villanueva@example.com'},
        {'first_name': 'Antonio', 'last_name': 'Cruz', 'date_of_birth': '1992-07-25', 'gender': 'Male', 'phone': '09177890123', 'email': 'antonio.cruz@example.com'},
        {'first_name': 'Carmen', 'last_name': 'Lopez', 'date_of_birth': '1988-09-14', 'gender': 'Female', 'phone': '09178901234', 'email': 'carmen.lopez@example.com'},
        {'first_name': 'Ricardo', 'last_name': 'Garcia', 'date_of_birth': '1970-02-28', 'gender': 'Male', 'phone': '09179012345', 'email': 'ricardo.garcia@example.com'},
        {'first_name': 'Teresa', 'last_name': 'Ramos', 'date_of_birth': '1983-10-08', 'gender': 'Female', 'phone': '09180123456', 'email': 'teresa.ramos@example.com'},
        {'first_name': 'Fernando', 'last_name': 'Aquino', 'date_of_birth': '1979-05-17', 'gender': 'Male', 'phone': '09181234567', 'email': 'fernando.aquino@example.com'},
        {'first_name': 'Lourdes', 'last_name': 'Mendoza', 'date_of_birth': '1993-01-23', 'gender': 'Female', 'phone': '09182345678', 'email': 'lourdes.mendoza@example.com'},
        {'first_name': 'Roberto', 'last_name': 'Castillo', 'date_of_birth': '1987-08-07', 'gender': 'Male', 'phone': '09183456789', 'email': 'roberto.castillo@example.com'},
        {'first_name': 'Sofia', 'last_name': 'Domingo', 'date_of_birth': '1991-11-19', 'gender': 'Female', 'phone': '09184567890', 'email': 'sofia.domingo@example.com'},
        {'first_name': 'Eduardo', 'last_name': 'Navarro', 'date_of_birth': '1980-04-03', 'gender': 'Male', 'phone': '09185678901', 'email': 'eduardo.navarro@example.com'},
        {'first_name': 'Isabel', 'last_name': 'Vargas', 'date_of_birth': '1976-12-27', 'gender': 'Female', 'phone': '09186789012', 'email': 'isabel.vargas@example.com'}
    ]

    # Additional sample data for other fields
    addresses = [
        "123 Ayala Avenue, Makati City",
        "456 Bonifacio Global City, Taguig",
        "789 Ortigas Center, Pasig City",
        "321 Alabang-Zapote Road, Muntinlupa",
        "654 Eastwood City, Quezon City",
        "987 Greenhills, San Juan"
    ]
    
    emergency_contacts = [
        ("Maria Reyes", "09171112222"),
        ("Juan Dela Cruz", "09172223333"),
        ("Ana Santos", "09173334444"),
        ("Pedro Bautista", "09174445555")
    ]
    
    medical_histories = [
        "Hypertension, controlled with medication",
        "Type 2 Diabetes, on oral medication",
        "Asthma, uses inhaler as needed",
        "No significant medical history",
        "Allergic to Penicillin"
    ]
    
    dental_histories = [
        "Regular dental check-ups, no major issues",
        "History of cavities, last filling 2 years ago",
        "Gingivitis, on maintenance cleaning every 6 months",
        "Previous root canal treatment",
        "Wears night guard for bruxism"
    ]
    
    allergies = [
        "No known allergies",
        "Allergic to Penicillin",
        "Latex allergy",
        "Local anesthesia allergy"
    ]
    
    insurance_providers = ["Maxicare", "MediCard", "PhilHealth", "Intellicare", "None"]

    # Create and add patients to the database
    with app.app_context():
        # Clear existing patients (optional, uncomment if needed)
        # Patient.query.delete()
        
        for data in patients_data:
            # Randomly select additional data
            address = choice(addresses)
            emergency_contact = choice(emergency_contacts)
            medical_history = choice(medical_histories)
            dental_history = choice(dental_histories)
            allergy = choice(allergies)
            has_insurance = choice([True, True, True, False])  # 75% chance of having insurance
            
            patient = Patient(
                first_name=data['first_name'],
                last_name=data['last_name'],
                date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date(),
                gender=data['gender'],
                phone=data['phone'],
                email=data['email'],
                address=address,
                emergency_contact_name=emergency_contact[0],
                emergency_contact_phone=emergency_contact[1],
                medical_history=medical_history,
                dental_history=dental_history,
                allergies=allergy,
                insurance_provider=choice(insurance_providers) if has_insurance else None,
                insurance_policy=f"POL{randint(100000, 999999)}" if has_insurance else None
            )
            
            db.session.add(patient)
        
        try:
            db.session.commit()
            print("Successfully added 16 sample patients to the database.")
            
            # Print the added patients
            patients = Patient.query.all()
            print("\nAdded patients:")
            for patient in patients:
                print(f"- {patient.first_name} {patient.last_name} (ID: {patient.id})")
                
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    create_sample_patients()
