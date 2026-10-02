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
    

def save_inventory(inventory):
    print("Saving inventory...")
    try:
        with open(FILENAME, "w") as file:
            json.dump(inventory, file, indent=4)
        print(f"Inventory saved successfully to {FILENAME}.\n")
    except IOError as e:
        print(f"Failed to save inventory: {e}\n")

def display_all(inventory):
    """Displays all products formatted in the catalog."""
    if not inventory:
        print("Inventory is currently empty.\n")
        return

    print("\nCurrent Inventory")
    for pid, details in inventory.items():
        print(f"ID: {pid} | Name: {details['name']} | Price: ${details['price']:.2f} | Stock: {details['stock']}")
    print()

def add_product(inventory):
    print("\nAdd New Product")
    pid = input("Product ID: ").strip()
    if pid in inventory:
        print("A product with this ID already exists!\n")
        return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())
    except ValueError:
        print("Invalid price or stock quantity. Operation aborted.\n")
        return

    inventory[pid] = {"name": name, "price": price, "stock": stock}
    print("Product added successfully!\n")

def update_stock(inventory):
    print("\nUpdate Stock")
    pid = input("Enter Product ID: ").strip()
    if pid not in inventory:
        print("Product not found.\n")
        return

    prod = inventory[pid]
    print(f"Product Found:\nName: {prod['name']}\nCurrent Stock: {prod['stock']}")
    
    try:
        new_stock = int(input("New Stock Quantity: ").strip())
        inventory[pid]["stock"] = new_stock
        print("Stock updated successfully!\n")
    except ValueError:
        print("Invalid number. Stock not updated.\n")

def search_product(inventory):
    print("\nSearch Product")
    pid = input("Enter Product ID: ").strip()
    if pid in inventory:
        prod = inventory[pid]
        print("Product Found")
        print("-" * 40)
        print(f"ID: {pid}\nName: {prod['name']}\nPrice: ${prod['price']:.2f}\nStock: {prod['stock']}")
        print("-" * 40 + "\n")
    else:
        print("Product not found.\n")



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