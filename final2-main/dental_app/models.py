from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from decimal import Decimal
from datetime import date


class Staff(AbstractUser):
    """Custom user model for staff members"""
    ROLE_CHOICES = [
        ('Administrator', 'Administrator'),
        ('Dentist', 'Dentist'),
        ('Hygienist', 'Dental Hygienist'),
        ('Assistant', 'Dental Assistant'),
        ('Receptionist', 'Receptionist'),
    ]
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Staff')
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"


class Patient(models.Model):
    """Patient model for storing patient information"""
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    medical_history = models.TextField(blank=True)
    dental_history = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    insurance_provider = models.CharField(max_length=100, blank=True)
    insurance_policy = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    
    def __str__(self):
        return self.get_full_name()
    
    class Meta:
        ordering = ['last_name', 'first_name']


class Appointment(models.Model):
    """Appointment model for scheduling patient appointments"""
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('No-Show', 'No-Show'),
    ]
    
    TYPE_CHOICES = [
        ('Check-up', 'Check-up'),
        ('Cleaning', 'Cleaning'),
        ('Filling', 'Filling'),
        ('Root Canal', 'Root Canal'),
        ('Extraction', 'Extraction'),
        ('Orthodontics', 'Orthodontics'),
        ('Emergency', 'Emergency'),
        ('Consultation', 'Consultation'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    duration = models.IntegerField(default=30, help_text="Duration in minutes")
    appointment_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.patient.get_full_name()} - {self.appointment_date} {self.appointment_time}"
    
    class Meta:
        ordering = ['appointment_date', 'appointment_time']


class Treatment(models.Model):
    """Treatment model for recording dental treatments"""
    STATUS_CHOICES = [
        ('Planned', 'Planned'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='treatments')
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='treatments')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='treatments')
    treatment_date = models.DateField()
    procedure_name = models.CharField(max_length=200)
    tooth_number = models.CharField(max_length=10, blank=True)
    diagnosis = models.TextField(blank=True)
    treatment_notes = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Planned')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.patient.get_full_name()} - {self.procedure_name}"
    
    class Meta:
        ordering = ['-treatment_date']


class Bill(models.Model):
    """Bill model for patient billing"""
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Overdue', 'Overdue'),
        ('Cancelled', 'Cancelled'),
        ('Partial', 'Partial'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('BDO Bank Transfer', 'BDO Bank Transfer'),
        ('Credit Card', 'Credit Card'),
        ('Check', 'Check'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='bills')
    bill_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_balance(self):
        return self.total_amount - self.paid_amount
    
    def __str__(self):
        return f"Bill #{self.id} - {self.patient.get_full_name()}"
    
    class Meta:
        ordering = ['-created_at']


class BillItem(models.Model):
    """Bill item model for individual line items in a bill"""
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.description} - {self.quantity}x ₱{self.unit_price}"


class InventoryItem(models.Model):
    """Inventory model for managing dental supplies"""
    CATEGORY_CHOICES = [
        ('Instruments', 'Instruments'),
        ('Materials', 'Materials'),
        ('Supplies', 'Supplies'),
        ('Equipment', 'Equipment'),
        ('Medications', 'Medications'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    current_stock = models.IntegerField(default=0)
    minimum_stock = models.IntegerField(default=10)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    supplier = models.CharField(max_length=100, blank=True)
    last_restocked = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_low_stock(self):
        return self.current_stock <= self.minimum_stock
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Communication(models.Model):
    """Communication model for patient communications"""
    TYPE_CHOICES = [
        ('Email', 'Email'),
        ('SMS', 'SMS'),
        ('Phone', 'Phone Call'),
        ('Letter', 'Letter'),
    ]
    
    STATUS_CHOICES = [
        ('Sent', 'Sent'),
        ('Failed', 'Failed'),
        ('Pending', 'Pending'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='communications')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Sent')
    
    def __str__(self):
        return f"{self.type} to {self.patient.get_full_name()} - {self.subject}"
    
    class Meta:
        ordering = ['-sent_at']