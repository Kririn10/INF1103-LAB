from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier
from inventory import Inventory
from order import Order
from product import Product

FILENAME = "inventory.json"


def show_product_details(product: Product) -> None:
    product.display_information()
    print(f"Fulfilment Details: {product.get_fulfilment_info()}")


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

        print("Supplier Details:")
        sup_id = input("  Supplier ID (e.g., SUP01): ").strip() or "SUP01"
        sup_name = input("  Supplier Name: ").strip() or "General Distributor"
        sup_email = input("  Supplier Email: ").strip() or "dist@example.com"
        supplier = Supplier(sup_id, sup_name, sup_email)

        if p_type == "1":
            weight = float(input("Weight (kg): ").strip())
            product = PhysicalProduct(pid, name, price, stock, weight, supplier)
        else:
            download_size = float(input("Download Size (MB): ").strip())
            product = DigitalProduct(pid, name, price, stock, download_size, supplier)

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

    print(f"Product Found: {product.name} | Current Stock: {product.stock}")
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
        show_product_details(product)
        print("-" * 50 + "\n")
    else:
        print("Product not found.\n")


def prompt_create_order(inventory: Inventory) -> None:
    print("\nCreate Customer Order (Composition Demo)")
    order_id = input("Enter Order ID (e.g., ORD1001): ").strip()
    order = Order(order_id)

    while True:
        pid = input("Enter Product ID to order (or 'done' to finish): ").strip()
        if pid.lower() == "done":
            break
        product = inventory.find_product(pid)
        if not product:
            print("Product not found in inventory. Try again.")
            continue
        try:
            qty = int(input(f"Enter quantity for {product.name}: ").strip())
            if qty <= 0:
                print("Quantity must be positive.")
                continue
            order.add_order_line(product, qty)
            print(f"Added {qty} x {product.name} to order.")
        except ValueError:
            print("Invalid integer quantity.")

    if order.order_lines:
        order.display_order_summary()
    else:
        print("Empty order discarded.\n")


def main() -> None:
    print("=" * 30)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 30)

    inventory = Inventory()
    inventory.load_from_file(FILENAME)

    while True:
        print("----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Create Customer Order")
        print("6. Save Inventory")
        print("7. Exit")
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
            prompt_create_order(inventory)
        elif choice == "6":
            inventory.save_to_file(FILENAME)
        elif choice == "7":
            print("\nSaving inventory before exit...")
            inventory.save_to_file(FILENAME)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid selection. Please choose an option between 1 and 7.\n")


if __name__ == "__main__":
    main()