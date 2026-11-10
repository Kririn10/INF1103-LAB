
import json
import os
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory

FILENAME = "inventory.json"






def prompt_add_product(inventory: Inventory) -> None:
    print("\nAdd New Product")
    print("Select Product Type:")
    print("1. Physical Product")
    print("2. Digital Product")
    p_type = input("Choice (1/2): ").strip()

    if p_type not in ("1", "2"):
        print("Invalid product type. Operation aborted.\n")
        return

    pid = input("Product ID: ").strip()
    if inventory.find_product(pid):
        print("A product with this ID already exists!\n")
        return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())

        if p_type == "1":
            weight = float(input("Weight (kg): ").strip())
            product = PhysicalProduct(pid, name, price, stock, weight)
        else:
            download_size = float(input("Download Size (MB): ").strip())
            product = DigitalProduct(pid, name, price, stock, download_size)

    except ValueError:
        print("Invalid numerical input. Operation aborted.\n")
        return

    if inventory.add_product(product):
        print("Product added successfully!\n")

def prompt_update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    pid = input("Enter Product ID: ").strip()
    product = inventory.find_product(pid)

    if not product:
        print("Product not found.\n")
        return

    print(f"Product Found:\nName: {product.name}\nCurrent Stock: {product.stock}")
    try:
        new_stock = int(input("New Stock Quantity: ").strip())
        product.update_stock(new_stock)
        print("Stock updated successfully!\n")
    except ValueError:
        print("Invalid number. Stock not updated.\n")


def prompt_search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    pid = input("Enter Product ID: ").strip()
    product = inventory.find_product(pid)

    if product:
        print("Product Found")
        print("-" * 50)
        product.display_information()
        print(f"Fulfilment Details: {product.get_fulfilment_info()}")
        print("-" * 50 + "\n")
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
            inventory.display_all()
        elif choice == "2":
            prompt_add_product(inventory)
        elif choice == "3":
            prompt_update_stock(inventory)
        elif choice == "4":
            prompt_search_product(inventory)
        elif choice == "5":
            inventory.save_to_file("inventory.json")
        elif choice == "6":
            print("\nSaving inventory before exit...")
            inventory.save_to_file("inventory.json")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid selection. Please choose an option between 1 and 6.")


if __name__ == "__main__":
    main()