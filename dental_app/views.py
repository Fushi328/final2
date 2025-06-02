from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from collections import Counter
import json
import calendar

def home(request):
    return HttpResponse("Welcome to the Dental App!")

@login_required
def dashboard(request):
    today = timezone.now().date()
    
    # Get today's appointments
    today_appointments = Appointment.objects.filter(
        appointment_date=today
    ).select_related('patient')
    
    # Calculate today's bookings count
    todays_bookings = today_appointments.count()
    
    # Calculate peak hour from today's appointments
    appointment_hours = []
    for apt in today_appointments:
        if apt.appointment_time:
            hour = apt.appointment_time.hour
            appointment_hours.append(hour)
    
    if appointment_hours:
        hour_counts = Counter(appointment_hours)
        peak_hour_24 = max(hour_counts, key=hour_counts.get)
        if peak_hour_24 == 0:
            peak_hour = "12:00 AM"
        elif peak_hour_24 < 12:
            peak_hour = f"{peak_hour_24}:00 AM"
        elif peak_hour_24 == 12:
            peak_hour = "12:00 PM"
        else:
            peak_hour = f"{peak_hour_24 - 12}:00 PM"
    else:
        peak_hour = "No appointments"
    
    # Calculate average daily appointments (last 30 days)
    thirty_days_ago = today - timedelta(days=30)
    total_appointments = Appointment.objects.filter(
        appointment_date__gte=thirty_days_ago,
        appointment_date__lte=today
    ).count()
    avg_daily = round(total_appointments / 30, 1) if total_appointments > 0 else 0
    
    # Get today's patient visits (appointments that are completed or in progress)
    patient_visits_today = today_appointments.filter(
        Q(status='completed') | Q(status='in_progress')
    ).count()
    
    # Get appointment trends data (last 7 months)
    appointment_trends = []
    for i in range(7):
        month_date = today.replace(day=1) - timedelta(days=30*i)
        month_appointments = Appointment.objects.filter(
            appointment_date__month=month_date.month,
            appointment_date__year=month_date.year
        ).count()
        appointment_trends.insert(0, {
            'month': calendar.month_abbr[month_date.month],
            'count': month_appointments
        })
    
    # Get appointment status distribution for pie chart
    appointment_status_data = []
    status_counts = Appointment.objects.filter(
        appointment_date__gte=today - timedelta(days=30)
    ).values('status').annotate(count=Count('status'))
    
    for status in status_counts:
        appointment_status_data.append({
            'status': status['status'].title(),
            'count': status['count']
        })
    
    # Get patient visits data (last 7 days)
    patient_visits_data = []
    for i in range(7):
        visit_date = today - timedelta(days=6-i)
        daily_visits = Appointment.objects.filter(
            appointment_date=visit_date,
            status__in=['completed', 'in_progress']
        ).count()
        patient_visits_data.append({
            'day': calendar.day_abbr[visit_date.weekday()],
            'visits': daily_visits
        })
    
    # Get inventory usage data
    inventory_categories = InventoryItem.objects.values('category').annotate(
        total_quantity=Sum('quantity'),
        total_items=Count('id')
    ).order_by('-total_quantity')
    
    inventory_usage_data = []
    for category in inventory_categories:
        if category['category']:
            inventory_usage_data.append({
                'category': category['category'].title(),
                'quantity': category['total_quantity'],
                'items': category['total_items']
            })
    
    # If no categories, create default data
    if not inventory_usage_data:
        inventory_usage_data = [
            {'category': 'Dental Supplies', 'quantity': 45, 'items': 12},
            {'category': 'Equipment', 'quantity': 30, 'items': 8},
            {'category': 'Medications', 'quantity': 25, 'items': 15}
        ]
    
    # Get recent appointments for the table
    recent_appointments = Appointment.objects.select_related('patient').order_by('-created_at')[:10]
    
    # Get low stock items
    low_stock_items = InventoryItem.objects.filter(quantity__lte=10).order_by('quantity')[:5]
    
    # Get total counts for overview cards
    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.count()
    total_treatments = Treatment.objects.count()
    total_staff = Staff.objects.count()
    
    context = {
        'todays_bookings': todays_bookings,
        'peak_hour': peak_hour,
        'avg_daily': avg_daily,
        'patient_visits_today': patient_visits_today,
        'recent_appointments': recent_appointments,
        'low_stock_items': low_stock_items,
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'total_treatments': total_treatments,
        'total_staff': total_staff,
        
        # Chart data
        'appointment_trends': json.dumps(appointment_trends),
        'appointment_status_data': json.dumps(appointment_status_data),
        'patient_visits_data': json.dumps(patient_visits_data),
        'inventory_usage_data': json.dumps(inventory_usage_data),
    }
    
    return render(request, 'reports/dashboard.html', context)
