from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Staff, Patient, Appointment, Treatment, Bill, BillItem, InventoryItem, Communication


@admin.register(Staff)
class StaffAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('last_name', 'first_name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone')}),
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'phone', 'email', 'date_of_birth', 'gender')
    list_filter = ('gender', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone', 'email')
    ordering = ('last_name', 'first_name')
    date_hierarchy = 'created_at'


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'staff', 'appointment_date', 'appointment_time', 'appointment_type', 'status')
    list_filter = ('status', 'appointment_type', 'appointment_date', 'staff')
    search_fields = ('patient__first_name', 'patient__last_name', 'staff__first_name', 'staff__last_name')
    ordering = ('-appointment_date', '-appointment_time')
    date_hierarchy = 'appointment_date'


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'procedure_name', 'treatment_date', 'cost', 'status', 'staff')
    list_filter = ('status', 'treatment_date', 'staff')
    search_fields = ('patient__first_name', 'patient__last_name', 'procedure_name')
    ordering = ('-treatment_date',)
    date_hierarchy = 'treatment_date'


class BillItemInline(admin.TabularInline):
    model = BillItem
    extra = 1


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'bill_date', 'total_amount', 'paid_amount', 'get_balance', 'status')
    list_filter = ('status', 'payment_method', 'bill_date')
    search_fields = ('patient__first_name', 'patient__last_name')
    ordering = ('-created_at',)
    date_hierarchy = 'bill_date'
    inlines = [BillItemInline]
    
    def get_balance(self, obj):
        return obj.get_balance()
    get_balance.short_description = 'Balance'


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'current_stock', 'minimum_stock', 'is_low_stock', 'supplier')
    list_filter = ('category', 'supplier')
    search_fields = ('name', 'description', 'supplier')
    ordering = ('name',)
    
    def is_low_stock(self, obj):
        return obj.is_low_stock()
    is_low_stock.boolean = True
    is_low_stock.short_description = 'Low Stock'


@admin.register(Communication)
class CommunicationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'type', 'subject', 'sent_at', 'status')
    list_filter = ('type', 'status', 'sent_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'subject')
    ordering = ('-sent_at',)
    date_hierarchy = 'sent_at'