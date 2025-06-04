from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, TimeField, IntegerField, DecimalField, PasswordField, BooleanField, EmailField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional
from datetime import datetime, date

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class PatientLoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class PatientForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=20)])
    email = EmailField('Email', validators=[Optional(), Email(), Length(max=120)])
    address = TextAreaField('Address')
    emergency_contact_name = StringField('Emergency Contact Name', validators=[Length(max=100)])
    emergency_contact_phone = StringField('Emergency Contact Phone', validators=[Length(max=20)])
    medical_history = TextAreaField('Medical History')
    dental_history = TextAreaField('Dental History')
    allergies = TextAreaField('Allergies')
    insurance_provider = StringField('Insurance Provider', validators=[Length(max=100)])
    insurance_policy = StringField('Insurance Policy Number', validators=[Length(max=100)])

class PatientRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    address = TextAreaField('Address')
    emergency_contact_name = StringField('Emergency Contact Name', validators=[Length(max=100)])
    emergency_contact_phone = StringField('Emergency Contact Phone', validators=[Length(max=20)])
    medical_history = TextAreaField('Medical History')
    dental_history = TextAreaField('Dental History')
    allergies = TextAreaField('Allergies')
    insurance_provider = StringField('Insurance Provider', validators=[Length(max=100)])
    insurance_policy = StringField('Insurance Policy Number', validators=[Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6)])

    def validate(self, extra_validators=None):
        rv = super().validate(extra_validators=extra_validators)
        if not rv:
            return False
        if self.password.data != self.confirm_password.data:
            self.confirm_password.errors.append('Passwords must match.')
            return False
        return True

class AppointmentForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    staff_id = SelectField('Staff Member', coerce=int, validators=[DataRequired()])
    appointment_date = DateField('Date', validators=[DataRequired()])
    appointment_time = TimeField('Time', validators=[DataRequired()])
    duration = SelectField('Duration', 
                          choices=[
                              (30, '30 minutes - Check-up/Cleaning'),
                              (60, '60 minutes - Filling/Simple Procedure'),
                              (90, '90 minutes - Root Canal/Extraction'),
                              (120, '120 minutes - Complex Procedure')
                          ], 
                          coerce=int, validators=[DataRequired()])
    appointment_type = SelectField('Appointment Type',
                                 choices=[
                                     ('Check-up', 'Check-up'),
                                     ('Cleaning', 'Cleaning'),
                                     ('Filling', 'Filling'),
                                     ('Root Canal', 'Root Canal'),
                                     ('Extraction', 'Extraction'),
                                     ('Orthodontics', 'Orthodontics'),
                                     ('Emergency', 'Emergency'),
                                     ('Consultation', 'Consultation')
                                 ], validators=[DataRequired()])
    notes = TextAreaField('Notes')

class PatientAppointmentForm(FlaskForm):
    appointment_date = DateField('Date', validators=[DataRequired()])
    appointment_time = TimeField('Time', validators=[DataRequired()])
    appointment_type = SelectField('Appointment Type',
                                 choices=[
                                     ('Check-up', 'Check-up'),
                                     ('Cleaning', 'Cleaning'),
                                     ('Filling', 'Filling'),
                                     ('Root Canal', 'Root Canal'),
                                     ('Extraction', 'Extraction'),
                                     ('Orthodontics', 'Orthodontics'),
                                     ('Emergency', 'Emergency'),
                                     ('Consultation', 'Consultation')
                                 ], validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[Optional()])

class TreatmentForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    staff_id = SelectField('Staff Member', coerce=int, validators=[DataRequired()])
    appointment_id = SelectField('Related Appointment', coerce=int, validators=[Optional()])
    treatment_date = DateField('Treatment Date', validators=[DataRequired()])
    procedure_name = StringField('Procedure Name', validators=[DataRequired(), Length(max=200)])
    tooth_number = StringField('Tooth Number', validators=[Length(max=10)])
    diagnosis = TextAreaField('Diagnosis')
    treatment_notes = TextAreaField('Treatment Notes')
    cost = DecimalField('Cost', validators=[DataRequired(), NumberRange(min=0)])
    status = SelectField('Status', 
                        choices=[('Planned', 'Planned'), ('In Progress', 'In Progress'), ('Completed', 'Completed')],
                        validators=[DataRequired()])

class BillForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[DataRequired()])
    payment_method = SelectField('Payment Method', 
                                choices=[('Cash', 'Cash'), ('BDO Bank Transfer', 'BDO Bank Transfer')],
                                validators=[Optional()])
    notes = TextAreaField('Notes')

class BillItemForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired(), Length(max=200)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    unit_price = DecimalField('Unit Price', validators=[DataRequired(), NumberRange(min=0)])

class PaymentForm(FlaskForm):
    amount = DecimalField('Payment Amount', validators=[DataRequired(), NumberRange(min=0)])
    payment_method = SelectField('Payment Method',
                                choices=[('Cash', 'Cash'), ('BDO Bank Transfer', 'BDO Bank Transfer')],
                                validators=[DataRequired()])
    notes = TextAreaField('Payment Notes')

class InventoryForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    category = SelectField('Category',
                          choices=[
                              ('Instruments', 'Instruments'),
                              ('Materials', 'Materials'),
                              ('Supplies', 'Supplies'),
                              ('Equipment', 'Equipment'),
                              ('Medications', 'Medications')
                          ], validators=[DataRequired()])
    current_stock = IntegerField('Current Stock', validators=[DataRequired(), NumberRange(min=0)])
    minimum_stock = IntegerField('Minimum Stock Level', validators=[DataRequired(), NumberRange(min=0)])
    unit_cost = DecimalField('Unit Cost', validators=[Optional(), NumberRange(min=0)])
    supplier = StringField('Supplier', validators=[Length(max=100)])
    last_restocked = DateField('Last Restocked', validators=[Optional()])

class StaffForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=64)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    role = SelectField('Role',
                      choices=[
                          ('Administrator', 'Administrator'),
                          ('Dentist', 'Dentist'),
                          ('Hygienist', 'Dental Hygienist'),
                          ('Assistant', 'Dental Assistant'),
                          ('Receptionist', 'Receptionist')
                      ], validators=[DataRequired()])
    phone = StringField('Phone', validators=[Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    is_active = BooleanField('Active', default=True)

class CommunicationForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    type = SelectField('Type', choices=[('Email', 'Email'), ('SMS', 'SMS')], validators=[DataRequired()])
    subject = StringField('Subject', validators=[Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired()])
