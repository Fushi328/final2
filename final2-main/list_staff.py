from app import create_app, db
from models import Staff

app = create_app()

with app.app_context():
    # Get all staff members
    all_staff = Staff.query.all()
    print(f"Found {len(all_staff)} staff members:")
    for staff in all_staff:
        print(f"- ID: {staff.id}, Username: {staff.username}, Email: {staff.email}, Role: {staff.role}")
