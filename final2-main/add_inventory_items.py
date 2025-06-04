from datetime import datetime
from app import app, db
from models import InventoryItem

def add_inventory_items():
    # Define the inventory items to add
    inventory_items = [
        {
            'name': 'Dental Gloves',
            'description': 'Disposable gloves for dental procedures',
            'category': 'Supplies',
            'current_stock': 5,  # Low stock
            'minimum_stock': 10,
            'unit_cost': 0.50,
            'supplier': 'Dental Supply Co.'
        },
        {
            'name': 'Anesthesia',
            'description': 'Local anesthesia for dental procedures',
            'category': 'Medications',
            'current_stock': 25,  # Good stock
            'minimum_stock': 10,
            'unit_cost': 5.00,
            'supplier': 'PharmaDent Inc.'
        },
        {
            'name': 'X-ray Films',
            'description': 'Dental X-ray films for imaging',
            'category': 'Supplies',
            'current_stock': 2,  # Critical stock
            'minimum_stock': 10,
            'unit_cost': 1.25,
            'supplier': 'Dental Imaging Solutions'
        }
    ]

    with app.app_context():
        # Check if items already exist
        for item_data in inventory_items:
            existing_item = InventoryItem.query.filter_by(name=item_data['name']).first()
            if existing_item:
                print(f"Item '{item_data['name']}' already exists in inventory.")
                continue
                
            # Create new inventory item
            item = InventoryItem(
                name=item_data['name'],
                description=item_data['description'],
                category=item_data['category'],
                current_stock=item_data['current_stock'],
                minimum_stock=item_data['minimum_stock'],
                unit_cost=item_data['unit_cost'],
                supplier=item_data['supplier'],
                last_restocked=datetime.now().date()
            )
            
            db.session.add(item)
        
        try:
            db.session.commit()
            print("Successfully added inventory items to the database.")
            
            # Print the added items
            print("\nAdded inventory items:")
            for item_data in inventory_items:
                item = InventoryItem.query.filter_by(name=item_data['name']).first()
                if item:
                    status = "Low" if item.is_low_stock() and item.current_stock > 0 else "Critical" if item.current_stock <= 0 else "Good"
                    print(f"- {item.name}: {status} (Stock: {item.current_stock}, Min: {item.minimum_stock})")
            
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    add_inventory_items()
