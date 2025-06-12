from app import create_app, db
from models import Staff

app = create_app()
with app.app_context():
    # Get all staff members
    all_staff = Staff.query.all()
    print(f"Found {len(all_staff)} staff members:")
    for staff in all_staff:
        print(f"- ID: {staff.id}, Username: {staff.username}, Email: {staff.email}, Role: {staff.role}")
    
    # Check if there are any duplicate usernames or emails
    from sqlalchemy import func
    
    # Check for duplicate usernames
    duplicate_usernames = db.session.query(
        Staff.username,
        func.count(Staff.username)
    ).group_by(Staff.username).having(func.count(Staff.username) > 1).all()
    
    # Check for duplicate emails
    duplicate_emails = db.session.query(
        Staff.email,
        func.count(Staff.email)
    ).group_by(Staff.email).having(func.count(Staff.email) > 1).all()
    
    print("\nDuplicate usernames:", duplicate_usernames)
    print("Duplicate emails:", duplicate_emails)
