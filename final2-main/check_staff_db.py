import sqlite3
import os

def check_staff_table():
    # Path to the SQLite database
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'dental_management.db')
    
    # If the database file doesn't exist, create it
    if not os.path.exists(db_path):
        print("Database file does not exist. Creating a new one...")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        open(db_path, 'a').close()
    
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if the staff table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='staff'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("Staff table does not exist in the database.")
            return
        
        # Get all records from the staff table
        cursor.execute("SELECT id, username, email, role FROM staff")
        staff_members = cursor.fetchall()
        
        if not staff_members:
            print("No staff members found in the database.")
        else:
            print(f"Found {len(staff_members)} staff members:")
            for staff in staff_members:
                print(f"- ID: {staff[0]}, Username: {staff[1]}, Email: {staff[2]}, Role: {staff[3]}")
        
        # Check for duplicate usernames
        cursor.execute("""
            SELECT username, COUNT(*) as count 
            FROM staff 
            GROUP BY username 
            HAVING count > 1
        """)
        duplicate_usernames = cursor.fetchall()
        
        # Check for duplicate emails
        cursor.execute("""
            SELECT email, COUNT(*) as count 
            FROM staff 
            WHERE email IS NOT NULL AND email != ''
            GROUP BY email 
            HAVING count > 1
        """)
        duplicate_emails = cursor.fetchall()
        
        if duplicate_usernames:
            print("\nDuplicate usernames found:")
            for username, count in duplicate_usernames:
                print(f"- Username '{username}' appears {count} times")
        
        if duplicate_emails:
            print("\nDuplicate emails found:")
            for email, count in duplicate_emails:
                print(f"- Email '{email}' appears {count} times")
        
        if not duplicate_usernames and not duplicate_emails and staff_members:
            print("\nNo duplicate usernames or emails found.")
            
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_staff_table()
