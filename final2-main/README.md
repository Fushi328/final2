# Dental Management System

A comprehensive dental practice management system built with Flask and SQLite for managing patient records, appointments, treatments, billing, and inventory.

## Features

- **Patient Management**: Digital patient records with search functionality
- **Appointment Scheduling**: Calendar view and appointment management
- **Treatment Recording**: Detailed treatment history and dental charts
- **Billing System**: Invoice generation with PDF export
- **Inventory Management**: Stock tracking with low stock alerts
- **Staff Management**: User roles and permissions
- **Reports & Analytics**: Dashboard with key metrics

## Quick Setup for Visual Studio Code

### Prerequisites
- Python 3.7 or higher
- Visual Studio Code with Python extension

### Installation Steps

1. **Clone or download the project files**

2. **Open the project in Visual Studio Code**

3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

4. **Install required packages**:
   ```bash
   pip install flask flask-sqlalchemy flask-login flask-wtf flask-mail werkzeug email-validator reportlab gunicorn wtforms sqlalchemy
   ```

5. **Initialize the database with sample data**:
   ```bash
   python setup.py
   ```

6. **Run the application**:
   ```bash
   python main.py
   ```

7. **Access the application**:
   Open your browser and go to `http://localhost:5000`

### Login Credentials
- **Username**: admin
- **Password**: admin123

## File Structure

```
dental-management-system/
├── app.py                 # Flask application configuration
├── main.py               # Application entry point
├── models.py             # Database models
├── routes.py             # URL routes and controllers
├── forms.py              # WTForms form definitions
├── utils.py              # Helper functions
├── setup.py              # Database initialization script
├── dental_management.sql # MySQL database schema (optional)
├── templates/            # HTML templates
├── static/               # CSS, JS, and image files
└── dental_management.db  # SQLite database (created automatically)
```

## Database

The system uses SQLite by default for easy setup. The database file (`dental_management.db`) is created automatically when you run the application for the first time.

If you prefer MySQL, you can:
1. Import the `dental_management.sql` file into your MySQL database
2. Update the database URI in `app.py`

## Usage

### Patient Management
- Add new patients with complete medical and dental history
- Search and filter patients
- View detailed patient profiles

### Appointments
- Schedule appointments with calendar view
- Manage appointment types and durations
- Track appointment status

### Treatments
- Record detailed treatment procedures
- Track costs and treatment status
- Link treatments to appointments

### Billing
- Generate invoices for treatments
- Track payments and outstanding balances
- Export invoices as PDF

### Inventory
- Manage dental supplies and equipment
- Set minimum stock levels
- Track suppliers and costs

### Reports
- View dashboard with key metrics
- Generate various reports
- Monitor practice performance

## Customization

The system can be customized by:
- Modifying the database models in `models.py`
- Adding new forms in `forms.py`
- Creating new routes in `routes.py`
- Updating templates in the `templates/` directory
- Styling with CSS in `static/css/style.css`

## Support

For technical support or questions about the system, please refer to the code documentation or contact your system administrator.