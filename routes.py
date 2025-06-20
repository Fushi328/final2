from flask import render_template, request, redirect, url_for, flash, jsonify, session, send_file
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date, timedelta
import os
import tempfile

from app import app, db, login_manager
from models import Staff, Patient, Appointment, Treatment, Bill, BillItem, InventoryItem, Communication
from forms import *
from utils import generate_invoice_pdf, send_appointment_reminder, get_dashboard_stats, get_upcoming_appointments, send_email, get_appointment_trends, get_inventory_usage_trends, get_patient_visits_hourly

@login_manager.user_loader
def load_user(user_id):
    return Staff.query.get(int(user_id))

# Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Staff.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.get_full_name()}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/api/dashboard-stats')
@login_required
def dashboard_stats():
    """API endpoint for dashboard updates"""
    try:
        # Get current stats
        stats = get_dashboard_stats()
        appointment_trends = get_appointment_trends()
        inventory_trends = get_inventory_usage_trends()
        patient_visits_hourly = get_patient_visits_hourly()
        
        # Get today's completed visits
        today_visits = Treatment.query.filter_by(
            treatment_date=date.today(),
            status='Completed'
        ).count()
        
        data = {
            'appointment_trends': appointment_trends,
            'today_visits': today_visits,
            'inventory_usage': inventory_trends[:5],  # Top 5 items
            'patient_visits_hourly': patient_visits_hourly,
            'stats': {
                'todays_appointments': stats['todays_appointments'],
                'avg_appointments_per_day': stats.get('avg_appointments_per_day', 0),
                'inventory_critical_count': stats['inventory_critical_count']
            }
        }
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

# Main Dashboard
@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    stats = get_dashboard_stats()
    upcoming_appointments = get_upcoming_appointments(7)
    return render_template('reports/dashboard.html', stats=stats, upcoming_appointments=upcoming_appointments)

# Patient Management Routes
@app.route('/patients')
@login_required
def patients_index():
    search = request.args.get('search', '')
    patients = Patient.query
    
    if search:
        patients = patients.filter(
            (Patient.first_name.contains(search)) |
            (Patient.last_name.contains(search)) |
            (Patient.phone.contains(search)) |
            (Patient.email.contains(search))
        )
    
    patients = patients.order_by(Patient.last_name, Patient.first_name).all()
    return render_template('patients/index.html', patients=patients, search=search)

@app.route('/patients/add', methods=['GET', 'POST'])
@login_required
def patients_add():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            date_of_birth=form.date_of_birth.data,
            gender=form.gender.data,
            phone=form.phone.data,
            email=form.email.data,
            address=form.address.data,
            emergency_contact_name=form.emergency_contact_name.data,
            emergency_contact_phone=form.emergency_contact_phone.data,
            medical_history=form.medical_history.data,
            dental_history=form.dental_history.data,
            allergies=form.allergies.data,
            insurance_provider=form.insurance_provider.data,
            insurance_policy=form.insurance_policy.data
        )
        db.session.add(patient)
        db.session.commit()
        flash(f'Patient {patient.get_full_name()} has been added successfully!', 'success')
        return redirect(url_for('patients_view', id=patient.id))
    return render_template('patients/add.html', form=form)

@app.route('/patients/<int:id>')
@login_required
def patients_view(id):
    patient = Patient.query.get_or_404(id)
    appointments = Appointment.query.filter_by(patient_id=id).order_by(Appointment.appointment_date.desc()).limit(10).all()
    treatments = Treatment.query.filter_by(patient_id=id).order_by(Treatment.treatment_date.desc()).limit(10).all()
    bills = Bill.query.filter_by(patient_id=id).order_by(Bill.bill_date.desc()).limit(10).all()
    return render_template('patients/view.html', patient=patient, appointments=appointments, treatments=treatments, bills=bills)

@app.route('/patients/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def patients_edit(id):
    patient = Patient.query.get_or_404(id)
    form = PatientForm(obj=patient)
    if form.validate_on_submit():
        form.populate_obj(patient)
        db.session.commit()
        flash(f'Patient {patient.get_full_name()} has been updated successfully!', 'success')
        return redirect(url_for('patients_view', id=patient.id))
    return render_template('patients/edit.html', form=form, patient=patient)

# Appointment Management Routes
@app.route('/appointments')
@login_required
def appointments_index():
    date_filter = request.args.get('date', date.today().strftime('%Y-%m-%d'))
    filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
    
    appointments = Appointment.query.filter_by(appointment_date=filter_date).order_by(Appointment.appointment_time).all()
    return render_template('appointments/index.html', appointments=appointments, filter_date=filter_date, timedelta=timedelta)

@app.route('/appointments/calendar')
@login_required
def appointments_calendar():
    # Get the filter_date from request arguments, default to today
    date_param = request.args.get('date', date.today().strftime('%Y-%m-%d'))
    try:
        filter_date = datetime.strptime(date_param, '%Y-%m-%d').date()
    except ValueError:
        filter_date = date.today()

    # Calculate start of current month and end of next month for data fetching
    start_of_current_month = date(filter_date.year, filter_date.month, 1)
    
    # Calculate the end of the next month
    if filter_date.month == 12:
        end_of_next_month = date(filter_date.year + 1, 2, 1) - timedelta(days=1) # Last day of January next year
    else:
        end_of_next_month = date(filter_date.year, filter_date.month + 2, 1) - timedelta(days=1) # Last day of the month after the current month

    appointments = Appointment.query.filter(
        Appointment.appointment_date >= start_of_current_month,
        Appointment.appointment_date <= end_of_next_month
    ).all()
    
    staff_members = Staff.query.filter_by(is_active=True).order_by(Staff.first_name).all()
    
    # Convert SQLAlchemy objects to dictionaries for JSON serialization
    appointments_data = [appointment.to_dict() for appointment in appointments]
    staff_members_data = [staff.to_dict() for staff in staff_members]

    return render_template('appointments/calendar.html', 
                           appointments=appointments_data, 
                           staff_members=staff_members_data, 
                           filter_date=filter_date)

@app.route('/appointments/add', methods=['GET', 'POST'])
@login_required
def appointments_add():
    form = AppointmentForm()
    form.patient_id.choices = [(p.id, p.get_full_name()) for p in Patient.query.order_by(Patient.last_name).all()]
    form.staff_id.choices = [(s.id, s.get_full_name()) for s in Staff.query.filter_by(is_active=True).all()]
    
    if form.validate_on_submit():
        appointment = Appointment(
            patient_id=form.patient_id.data,
            staff_id=form.staff_id.data,
            appointment_date=form.appointment_date.data,
            appointment_time=form.appointment_time.data,
            duration=form.duration.data,
            appointment_type=form.appointment_type.data,
            notes=form.notes.data
        )
        db.session.add(appointment)
        db.session.commit()
        
        # Send appointment confirmation email
        if appointment.patient.email:
            send_appointment_reminder(appointment)
        
        flash(f'Appointment scheduled for {appointment.patient.get_full_name()} on {appointment.appointment_date}', 'success')
        return redirect(url_for('appointments_index'))
    
    return render_template('appointments/add.html', form=form)

# Treatment Management Routes
@app.route('/treatments')
@login_required
def treatments_index():
    search = request.args.get('search', '')
    treatments = Treatment.query.join(Patient)
    
    if search:
        treatments = treatments.filter(
            (Patient.first_name.contains(search)) |
            (Patient.last_name.contains(search)) |
            (Treatment.procedure_name.contains(search))
        )
    
    treatments = treatments.order_by(Treatment.treatment_date.desc()).all()
    return render_template('treatments/index.html', treatments=treatments, search=search)

@app.route('/treatments/add', methods=['GET', 'POST'])
@login_required
def treatments_add():
    form = TreatmentForm()
    form.patient_id.choices = [(p.id, p.get_full_name()) for p in Patient.query.order_by(Patient.last_name).all()]
    form.staff_id.choices = [(s.id, s.get_full_name()) for s in Staff.query.filter_by(is_active=True).all()]
    form.appointment_id.choices = [(0, 'No related appointment')] + [(a.id, f"{a.appointment_date} - {a.appointment_type}") for a in Appointment.query.order_by(Appointment.appointment_date.desc()).limit(20).all()]
    
    if form.validate_on_submit():
        treatment = Treatment(
            patient_id=form.patient_id.data,
            staff_id=form.staff_id.data,
            appointment_id=form.appointment_id.data if form.appointment_id.data != 0 else None,
            treatment_date=form.treatment_date.data,
            procedure_name=form.procedure_name.data,
            tooth_number=form.tooth_number.data,
            diagnosis=form.diagnosis.data,
            treatment_notes=form.treatment_notes.data,
            cost=form.cost.data,
            status=form.status.data
        )
        db.session.add(treatment)
        db.session.commit()
        flash(f'Treatment record added for {treatment.patient.get_full_name()}', 'success')
        return redirect(url_for('treatments_index'))
    
    return render_template('treatments/add.html', form=form)

# Billing Routes
@app.route('/billing')
@login_required
def billing_index():
    status_filter = request.args.get('status', 'all')
    bills = Bill.query.join(Patient)
    
    if status_filter != 'all':
        bills = bills.filter(Bill.status == status_filter)
    
    bills = bills.order_by(Bill.bill_date.desc()).all()
    today = date.today()
    return render_template('billing/index.html', bills=bills, status_filter=status_filter, today=today)

@app.route('/billing/add', methods=['GET', 'POST'])
@login_required
def billing_add():
    form = BillForm()
    form.patient_id.choices = [(p.id, p.get_full_name()) for p in Patient.query.order_by(Patient.last_name).all()]

    if form.validate_on_submit():
        try:
            bill = Bill(
                patient_id=form.patient_id.data,
                bill_date=date.today(),
                due_date=form.due_date.data,
                payment_method=form.payment_method.data,
                notes=form.notes.data,
                status='Pending',
                total_amount=0
            )
            db.session.add(bill)
            db.session.flush() # To get bill.id before commit

            total_amount = 0
            item_count_str = request.form.get('item_count', '0')
            try:
                item_count = int(item_count_str)
            except (ValueError, TypeError):
                item_count = 0

            for i in range(item_count):
                description = request.form.get(f'items[{i}][description]', '')
                
                quantity_str = request.form.get(f'items[{i}][quantity]', '0')
                try:
                    quantity = int(quantity_str)
                except (ValueError, TypeError):
                    quantity = 0
                
                unit_price_str = request.form.get(f'items[{i}][unit_price]', '0.0')
                try:
                    unit_price = float(unit_price_str)
                except (ValueError, TypeError):
                    unit_price = 0.0
                
                total_price_str = request.form.get(f'items[{i}][total_price]', '0.0')
                try:
                    total_price = float(total_price_str)
                except (ValueError, TypeError):
                    total_price = 0.0

                if description and quantity > 0 and unit_price >= 0:
                    item = BillItem(
                        bill_id=bill.id,
                        description=description,
                        quantity=quantity,
                        unit_price=unit_price,
                        total_price=total_price
                    )
                    db.session.add(item)
                    total_amount += total_price

            bill.total_amount = total_amount
            db.session.commit()

            flash(f'Bill for {bill.patient.get_full_name()} created successfully! Bill ID: {bill.id}', 'success')
            
            if bill.payment_method == 'GCash':
                return redirect(url_for('gcash_qr_payment', id=bill.id))
            elif bill.payment_method == 'BDO Bank Transfer':
                return redirect(url_for('bdo_qr_payment', id=bill.id))
            else:
                return redirect(url_for('billing_view', id=bill.id))

        except Exception as e:
            db.session.rollback()
            flash(f'Error creating bill: {str(e)}', 'danger')
            # Re-populate form choices in case of an error
            form.patient_id.choices = [(p.id, p.get_full_name()) for p in Patient.query.order_by(Patient.last_name).all()]
            return render_template('billing/add.html', form=form)
    
    # For GET request or if form validation fails
    form.patient_id.choices = [(p.id, p.get_full_name()) for p in Patient.query.order_by(Patient.last_name).all()]
    return render_template('billing/add.html', form=form)

@app.route('/billing/<int:id>')
@login_required
def billing_view(id):
    bill = Bill.query.get_or_404(id)
    return render_template('billing/invoice.html', bill=bill)

@app.route('/billing/<int:id>/pdf')
@login_required
def billing_pdf(id):
    bill = Bill.query.get_or_404(id)
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        if generate_invoice_pdf(bill, tmp_file.name):
            return send_file(tmp_file.name, as_attachment=True, 
                           download_name=f'invoice_{bill.id}.pdf', mimetype='application/pdf')
        else:
            flash('Error generating PDF', 'danger')
            return redirect(url_for('billing_view', id=id))

@app.route('/billing/<int:id>/gcash_qr')
@login_required
def gcash_qr_payment(id):
    bill = Bill.query.get_or_404(id)
    return render_template('billing/gcash_qr.html', bill=bill)

@app.route('/billing/<int:id>/bdo_qr')
@login_required
def bdo_qr_payment(id):
    bill = Bill.query.get_or_404(id)
    if bill.payment_method != 'BDO Bank Transfer':
        flash('Invalid payment method for BDO QR code.', 'danger')
        return redirect(url_for('billing_view', id=bill.id))
    return render_template('billing/bdo_qr.html', bill=bill)

@app.route('/billing/<int:id>/confirm_payment', methods=['POST'])
@login_required
def confirm_payment(id):
    bill = Bill.query.get_or_404(id)
    bill.status = 'Paid'
    bill.paid_amount = bill.total_amount  # Assuming full payment via QR
    bill.payment_method = 'GCash QR'
    db.session.commit()
    flash(f'Bill INV-{bill.id:04d} has been marked as Paid via GCash QR.', 'success')
    return redirect(url_for('billing_view', id=bill.id))

@app.route('/billing/<int:id>/pay', methods=['POST'])
@login_required
def billing_pay():
    bill_id = request.json.get('bill_id')
    amount = float(request.json.get('amount', 0))
    payment_method = request.json.get('payment_method')
    
    bill = Bill.query.get_or_404(bill_id)
    bill.paid_amount = float(bill.paid_amount) + amount
    bill.payment_method = payment_method
    
    if bill.paid_amount >= float(bill.total_amount):
        bill.status = 'Paid'
    
    db.session.commit()
    return jsonify({'success': True, 'new_balance': bill.get_balance()})

# Inventory Routes
@app.route('/inventory')
@login_required
def inventory_index():
    category_filter = request.args.get('category', 'all')
    items = InventoryItem.query
    
    if category_filter != 'all':
        items = items.filter(InventoryItem.category == category_filter)
    
    items = items.order_by(InventoryItem.name).all()
    categories = db.session.query(InventoryItem.category).distinct().all()
    return render_template('inventory/index.html', items=items, categories=categories, category_filter=category_filter)

@app.route('/inventory/add', methods=['GET', 'POST'])
@login_required
def inventory_add():
    form = InventoryForm()
    if form.validate_on_submit():
        item = InventoryItem(
            name=form.name.data,
            description=form.description.data,
            category=form.category.data,
            current_stock=form.current_stock.data,
            minimum_stock=form.minimum_stock.data,
            unit_cost=form.unit_cost.data,
            supplier=form.supplier.data,
            last_restocked=form.last_restocked.data
        )
        db.session.add(item)
        db.session.commit()
        flash(f'Inventory item "{item.name}" has been added successfully!', 'success')
        return redirect(url_for('inventory_index'))
    return render_template('inventory/add.html', form=form)

# Staff Management Routes
@app.route('/staff')
@login_required
def staff_index():
    staff_members = Staff.query.order_by(Staff.last_name, Staff.first_name).all()
    
    today = date.today()
    # Calculate the start of the current week (Monday)
    week_start = today - timedelta(days=today.weekday())
    
    return render_template('staff/index.html', staff_members=staff_members, today=today, week_start=week_start)

@app.route('/staff/add', methods=['GET', 'POST'])
@login_required
def staff_add():
    form = StaffForm()
    if form.validate_on_submit():
        # Check if username or email already exists
        existing_staff = Staff.query.filter(
            (Staff.username == form.username.data) | 
            (Staff.email == form.email.data)
        ).first()
        
        if existing_staff:
            flash('Username or email already exists!', 'danger')
        else:
            staff = Staff(
                username=form.username.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                role=form.role.data,
                phone=form.phone.data,
                password_hash=generate_password_hash(form.password.data),
                is_active=form.is_active.data
            )
            db.session.add(staff)
            db.session.commit()
            flash(f'Staff member {staff.get_full_name()} has been added successfully!', 'success')
            return redirect(url_for('staff_index'))
    return render_template('staff/add.html', form=form)

# Reports and Analytics
@app.route('/reports')
@login_required
def reports_dashboard():
    return render_template('reports/dashboard.html')

# Communication Routes
@app.route('/communication/send', methods=['POST'])
@login_required
def send_communication():
    patient_id = request.json.get('patient_id')
    message_type = request.json.get('type')
    subject = request.json.get('subject', '')
    message = request.json.get('message')
    
    patient = Patient.query.get_or_404(patient_id)
    
    success = False
    if message_type == 'Email' and patient.email:
        success = send_email(patient.email, subject, message, patient.get_full_name())
    elif message_type == 'SMS' and patient.phone:
        # SMS functionality would need SMS API integration
        flash('SMS functionality not yet implemented', 'warning')
        success = False
    
    if success:
        communication = Communication(
            patient_id=patient_id,
            type=message_type,
            subject=subject,
            message=message,
            status='Sent'
        )
        db.session.add(communication)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Message sent successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to send message'})

# API Endpoints for AJAX requests
@app.route('/api/patients/search')
@login_required
def api_patients_search():
    query = request.args.get('q', '')
    patients = Patient.query.filter(
        (Patient.first_name.contains(query)) |
        (Patient.last_name.contains(query))
    ).limit(10).all()
    
    return jsonify([{
        'id': p.id,
        'name': p.get_full_name(),
        'phone': p.phone
    } for p in patients])

@app.route('/api/appointments/check')
@login_required
def api_check_appointment_conflicts():
    date_str = request.args.get('date')
    time_str = request.args.get('time')
    staff_id = request.args.get('staff_id')
    duration = int(request.args.get('duration', 30))
    
    appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    appointment_time = datetime.strptime(time_str, '%H:%M').time()
    
    # Check for conflicts
    conflicts = Appointment.query.filter(
        Appointment.appointment_date == appointment_date,
        Appointment.staff_id == staff_id,
        Appointment.status == 'Scheduled'
    ).all()
    
    has_conflict = False
    for conflict in conflicts:
        # Simple time conflict check
        conflict_end = datetime.combine(appointment_date, conflict.appointment_time)
        conflict_end = conflict_end + timedelta(minutes=conflict.duration)
        
        appointment_start = datetime.combine(appointment_date, appointment_time)
        appointment_end = appointment_start + timedelta(minutes=duration)
        
        if (appointment_start < conflict_end and appointment_end > datetime.combine(appointment_date, conflict.appointment_time)):
            has_conflict = True
            break
    
    return jsonify({'has_conflict': has_conflict})

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
