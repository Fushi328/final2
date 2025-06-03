from app import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import text

class Staff(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='Staff')
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'phone': self.phone,
            'is_active': self.is_active,
            'full_name': self.get_full_name()
        }

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(20))
    medical_history = db.Column(db.Text)
    dental_history = db.Column(db.Text)
    allergies = db.Column(db.Text)
    insurance_provider = db.Column(db.String(100))
    insurance_policy = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    treatments = db.relationship('Treatment', backref='patient', lazy=True)
    bills = db.relationship('Bill', backref='patient', lazy=True)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_age(self):
        today = datetime.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat(),
            'gender': self.gender,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'full_name': self.get_full_name()
        }

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    duration = db.Column(db.Integer, nullable=False, default=30)  # Duration in minutes
    appointment_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='Scheduled')  # Scheduled, Completed, Cancelled, No-Show
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    staff = db.relationship('Staff', backref='appointments')

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'staff_id': self.staff_id,
            'appointment_date': self.appointment_date.isoformat(),
            'appointment_time': self.appointment_time.isoformat(timespec='minutes'),
            'duration': self.duration,
            'appointment_type': self.appointment_type,
            'status': self.status,
            'notes': self.notes,
            'patient': self.patient.to_dict() if self.patient else None, # Include patient data
            'staff': self.staff.to_dict() if self.staff else None # Include staff data
        }

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    treatment_date = db.Column(db.Date, nullable=False)
    procedure_name = db.Column(db.String(200), nullable=False)
    tooth_number = db.Column(db.String(10))
    diagnosis = db.Column(db.Text)
    treatment_notes = db.Column(db.Text)
    cost = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='Planned')  # Planned, In Progress, Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    staff = db.relationship('Staff', backref='treatments')
    appointment = db.relationship('Appointment', backref='treatments')

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    bill_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.Date, nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    paid_amount = db.Column(db.Numeric(10, 2), default=0)
    status = db.Column(db.String(20), default='Pending')  # Pending, Paid, Overdue, Cancelled
    payment_method = db.Column(db.String(50))  # Cash, BDO Bank Transfer
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bill_items = db.relationship('BillItem', backref='bill', lazy=True, cascade='all, delete-orphan')
    
    def get_balance(self):
        return float(self.total_amount) - float(self.paid_amount)

class BillItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    current_stock = db.Column(db.Integer, nullable=False, default=0)
    minimum_stock = db.Column(db.Integer, nullable=False, default=10)
    unit_cost = db.Column(db.Numeric(10, 2))
    supplier = db.Column(db.String(100))
    last_restocked = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def is_low_stock(self):
        return self.current_stock <= self.minimum_stock

class Communication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # Email, SMS
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Sent')  # Sent, Failed, Pending
    
    # Relationships
    patient = db.relationship('Patient', backref='communications')
