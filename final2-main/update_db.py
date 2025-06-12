from app import app, db
from models import Staff, Patient, Appointment, Treatment, Bill, BillItem, InventoryItem, Communication

def update_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if the photo column exists in the staff table
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        columns = [column['name'] for column in inspector.get_columns('staff')]
        
        if 'photo' not in columns:
            print("Adding 'photo' column to staff table...")
            db.engine.execute('ALTER TABLE staff ADD COLUMN photo VARCHAR(255)')
            print("Database updated successfully!")
        else:
            print("The 'photo' column already exists in the staff table.")

if __name__ == '__main__':
    update_database()
