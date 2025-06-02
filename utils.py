import os
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from flask_mail import Message
from app import mail
import logging

def generate_invoice_pdf(bill, filename):
    """Generate a PDF invoice for a bill"""
    try:
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        story.append(Paragraph("DENTAL CLINIC INVOICE", title_style))
        story.append(Spacer(1, 20))

        # Clinic and patient info
        info_data = [
            ['Bill #:', str(bill.id)],
            ['Date:', bill.bill_date.strftime('%B %d, %Y')],
            ['Due Date:', bill.due_date.strftime('%B %d, %Y')],
            ['Patient:', bill.patient.get_full_name()],
            ['Patient Phone:', bill.patient.phone],
            ['Patient Email:', bill.patient.email or 'N/A']
        ]

        info_table = Table(info_data, colWidths=[1.5*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#34495e')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 30))

        # Services table
        services_data = [['Description', 'Quantity', 'Unit Price', 'Total']]
        for item in bill.bill_items:
            services_data.append([
                item.description,
                str(item.quantity),
                f"₱{item.unit_price:,.2f}",
                f"₱{item.total_price:,.2f}"
            ])

        # Add totals
        services_data.append(['', '', 'Subtotal:', f"₱{bill.total_amount:,.2f}"])
        if bill.paid_amount > 0:
            services_data.append(['', '', 'Paid:', f"₱{bill.paid_amount:,.2f}"])
            services_data.append(['', '', 'Balance:', f"₱{bill.get_balance():,.2f}"])

        services_table = Table(services_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
        services_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, -3), (-1, -1), colors.HexColor('#ecf0f1')),
        ]))
        story.append(services_table)
        story.append(Spacer(1, 30))

        # Payment information
        if bill.payment_method:
            payment_info = f"Payment Method: {bill.payment_method}"
            story.append(Paragraph(payment_info, styles['Normal']))

        if bill.notes:
            story.append(Spacer(1, 20))
            story.append(Paragraph(f"Notes: {bill.notes}", styles['Normal']))

        # Build PDF
        doc.build(story)
        return True
    except Exception as e:
        logging.error(f"Error generating PDF: {str(e)}")
        return False

def send_email(to_email, subject, body, patient_name=None):
    """Send email to patient"""
    try:
        msg = Message(
            subject=subject,
            recipients=[to_email],
            body=body
        )
        mail.send(msg)
        return True
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
        return False

def send_appointment_reminder(appointment):
    """Send appointment reminder email"""
    if not appointment.patient.email:
        return False

    subject = "Appointment Reminder - Dental Clinic"
    body = f"""
Dear {appointment.patient.get_full_name()},

This is a reminder for your upcoming dental appointment:

Date: {appointment.appointment_date.strftime('%B %d, %Y')}
Time: {appointment.appointment_time.strftime('%I:%M %p')}
Type: {appointment.appointment_type}
Duration: {appointment.duration} minutes
Doctor: Dr. {appointment.staff.get_full_name()}

Please arrive 15 minutes early for check-in.

If you need to reschedule or cancel, please contact us as soon as possible.

Best regards,
Dental Clinic Team
"""

    return send_email(appointment.patient.email, subject, body, appointment.patient.get_full_name())

def get_dashboard_stats():
    """Get statistics for dashboard"""
    from models import Patient, Appointment, Bill, InventoryItem, Treatment
    from datetime import date, timedelta

    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)

    stats = {
        'total_patients': Patient.query.count(),
        'todays_appointments': Appointment.query.filter_by(appointment_date=today).count(),
        'this_week_appointments': Appointment.query.filter(
            Appointment.appointment_date >= week_start,
            Appointment.appointment_date <= today
        ).count(),
        'pending_bills': Bill.query.filter_by(status='Pending').count(),
        'low_stock_items': InventoryItem.query.filter(
            InventoryItem.current_stock <= InventoryItem.minimum_stock
        ).count(),
        'total_revenue_month': 0,
        'completed_treatments_today': Treatment.query.filter_by(
            treatment_date=today, 
            status='Completed'
        ).count(),
        'avg_appointments_per_day': 0,
        'inventory_critical_count': InventoryItem.query.filter(
            InventoryItem.current_stock <= (InventoryItem.minimum_stock * 0.1)
        ).count()
    }

    # Calculate monthly revenue
    monthly_bills = Bill.query.filter(
        Bill.bill_date >= month_start,
        Bill.status == 'Paid'
    ).all()

    stats['total_revenue_month'] = sum(float(bill.paid_amount) for bill in monthly_bills)

    # Calculate average appointments per day
    total_appointments = Appointment.query.count()
    if total_appointments > 0:
        first_appointment = Appointment.query.order_by(Appointment.created_at.asc()).first()
        if first_appointment:
            days_since_first = (today - first_appointment.created_at.date()).days + 1
            stats['avg_appointments_per_day'] = round(total_appointments / max(days_since_first, 1), 1)

    return statshly_bills)

    # Calculate average appointments per day (last 30 days)
    past_30_days = today - timedelta(days=30)
    total_appointments_30_days = Appointment.query.filter(
        Appointment.appointment_date >= past_30_days,
        Appointment.appointment_date <= today
    ).count()

    stats['avg_appointments_per_day'] = round(total_appointments_30_days / 30, 1)

    return stats

def get_realtime_appointment_trends():
    """Get appointment trends for the last 7 days"""
    from datetime import date, timedelta
    from models import Appointment
    from app import db

    try:
        trends = []
        today = date.today()

        for i in range(7):
            target_date = today - timedelta(days=i)
            count = Appointment.query.filter_by(appointment_date=target_date).count()
            trends.append({
                'date': target_date.strftime('%Y-%m-%d'),
                'day': target_date.strftime('%a'),
                'count': count
            })

        return list(reversed(trends))
    except Exception as e:
        print(f"Error getting appointment trends: {e}")
        return []

def get_inventory_usage_trends():
    """Get inventory items with usage statistics"""
    from models import InventoryItem
    from app import db

    try:
        # Get all items and calculate usage percentage
        items = InventoryItem.query.all()

        usage_data = []
        for item in items:
            if item.minimum_stock > 0:
                usage_percentage = round((item.minimum_stock - item.current_stock) / item.minimum_stock * 100, 1)
                if usage_percentage < 0:
                    usage_percentage = 0
            else:
                usage_percentage = 0

            usage_data.append({
                'name': item.name,
                'current_stock': item.current_stock,
                'minimum_stock': item.minimum_stock,
                'usage_percentage': usage_percentage,
                'is_low_stock': item.current_stock <= item.minimum_stock,
                'category': item.category
            })

        # Sort by usage percentage (highest first)
        return sorted(usage_data, key=lambda x: x['usage_percentage'], reverse=True)
    except Exception as e:
        print(f"Error getting inventory usage: {e}")
        return []

def get_upcoming_appointments(days=7):
    """Get upcoming appointments for the next few days"""
    from models import Appointment
    from datetime import date, timedelta

    today = date.today()
    end_date = today + timedelta(days=days)

    return Appointment.query.filter(
        Appointment.appointment_date >= today,
        Appointment.appointment_date <= end_date,
        Appointment.status == 'Scheduled'
    ).order_by(Appointment.appointment_date, Appointment.appointment_time).all()ime).all()

def format_currency(amount):
    """Format amount as currency"""
    return f"₱{float(amount):,.2f}"

def calculate_age(birth_date):
    """Calculate age from birth date"""
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))