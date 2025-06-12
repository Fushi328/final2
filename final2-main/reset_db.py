from app import app, db
from models import Staff
from werkzeug.security import generate_password_hash

def reset_database():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        
        # Create all tables with the new schema
        db.create_all()
        
        # Check if admin user exists
        admin = Staff.query.filter_by(username='admin').first()
        if not admin:
            # Create admin user
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
            print("Database reset successfully! Admin user created.")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    reset_database()
