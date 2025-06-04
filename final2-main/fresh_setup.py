from app import app, db
from models import Staff, Patient, Appointment, Treatment, Bill, BillItem, InventoryItem, Communication
from werkzeug.security import generate_password_hash

def setup_database():
    with app.app_context():
        # Drop all existing tables
        print("Dropping all tables...")
        db.drop_all()
        
        # Create all tables
        print("Creating tables...")
        db.create_all()
        
        # Create admin user
        print("Creating admin user...")
        admin = Staff(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            first_name='Admin',
            last_name='User',
            role='Administrator',
            phone='1234567890',
            photo=None,
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        
        print("Database setup complete!")
        print("Admin username: admin")
        print("Admin password: admin123")

if __name__ == '__main__':
    setup_database()
