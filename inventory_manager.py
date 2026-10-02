import json
import os

FILENAME = "inventory.json"
def load_inventory():
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                data = json.load(file)
                print("inventory.json found.")
                print("Inventory loaded successfully.\n")
                return data
        except (json.JSONDecodeError, IOError):
            print("Error loading inventory file. Starting with default inventory.\n")

    # Initial default dataset if file doesn't exist
    return {
        "P001": {"name": "Laptop", "price": 1200.00, "stock": 15},
        "P002": {"name": "Mouse", "price": 25.50, "stock": 40},
        "P003": {"name": "Keyboard", "price": 45.00, "stock": 25}
    }


def main():
    print("=" * 30)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 30)
    
    inventory = load_inventory()

    while True:
        print("----------- MENU ----------- ")
        print("1. Display All Products\n2. Add Product\n3. Update Stock\n4. Search Product\n5. Save Inventory\n6. Exit")
        print("----------------------------")
        
        choice = input("Enter option: ").strip()

        if choice == "1":
            display_all(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid selection. Please choose an option between 1 and 6.\n")

if __name__ == "__main__":
    main()