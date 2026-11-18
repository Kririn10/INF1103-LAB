import csv
from supplier import Supplier
from inventory import Inventory
from order import Order
from product import Product
from product_factory import ProductFactory
from discount_strategy import (
    NoDiscount,
    PercentageDiscount,
    BulkDiscount,
    StudentDiscount,
)

FILENAME = "inventory.json"
CSV_FILENAME = "products.csv"


def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    loaded = 0
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header row
            for row in reader:
                try:
                    if len(row) < 5:
                        raise ValueError("Incomplete row data")
                    product_type = row[0].strip()
                    product_id = row[1].strip()
                    name = row[2].strip()
                    price = float(row[3].strip())
                    stock_quantity = int(row[4].strip())

                    product = ProductFactory.create(
                        product_type,
                        product_id,
                        name,
                        price,
                        stock_quantity,
                        supplier,
                    )
                    if inventory.add_product(product):
                        loaded += 1
                except ValueError as e:
                    print(f"Skipping invalid row {row}: {e}")
                    continue
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


def show_product_details(product: Product) -> None:
    product.display_information()
    print(f"Fulfilment Details: {product.get_fulfilment_info()}")


def prompt_add_product(inventory: Inventory) -> None:
    print("\nAdd New Product")
    print("Select Product Type:")
    print("1. Physical Product")
    print("2. Digital Product")
    p_choice = input("Choice (1/2): ").strip()

    if p_choice == "1":
        p_type = "physical"
    elif p_choice == "2":
        p_type = "digital"
    else:
        print("Invalid product type. Operation aborted.\n")
        return

    pid = input("Product ID: ").strip()
    if inventory.find_product(pid):
        print("A product with this ID already exists!\n")
        return

    name = input("Product Name: ").strip()
    price = get_positive_float("Price: ")

    try:
        stock = int(input("Stock Quantity: ").strip())

        print("Supplier Details:")
        sup_id = input("  Supplier ID (e.g., SUP01): ").strip() or "SUP01"
        sup_name = (
            input("  Supplier Name: ").strip() or "General Distributor"
        )
        sup_email = (
            input("  Supplier Email: ").strip() or "dist@example.com"
        )
        supplier = Supplier(sup_id, sup_name, sup_email)

        if p_type == "physical":
            weight = get_positive_float("Weight (kg): ")
            product = ProductFactory.create(
                p_type, pid, name, price, stock, supplier, weight=weight
            )
        else:
            download_size = get_positive_float("Download Size (MB): ")
            product = ProductFactory.create(
                p_type,
                pid,
                name,
                price,
                stock,
                supplier,
                download_size=download_size,
            )

    except ValueError as e:
        print(f"Invalid input ({e}). Operation aborted.\n")
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
    except ValueError as e:
        print(f"Invalid stock update: {e}\n")


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
    print("\nCreate Customer Order")
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
            order.add_order_line(product, qty)
            print(f"Added {qty} x {product.name} to order.")
        except ValueError as e:
            print(f"Invalid quantity: {e}")

    if order.order_lines:
        print("\nSelect Discount Strategy:")
        print("1. No Discount")
        print("2. Percentage Discount (10%)")
        print("3. Bulk Discount ($20 off orders >= $200)")
        print("4. Student Discount (5%)")
        d_choice = input("Choice (1-4): ").strip()

        if d_choice == "2":
            order.set_discount(PercentageDiscount(10))
        elif d_choice == "3":
            order.set_discount(BulkDiscount(200, 20))
        elif d_choice == "4":
            order.set_discount(StudentDiscount())
        else:
            order.set_discount(NoDiscount())

        order.display_order_summary()
    else:
        print("Empty order discarded.\n")


def main() -> None:
    print("=" * 30)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 30)

    inventory = Inventory()
    inventory.load_from_file(FILENAME)
    default_supplier = Supplier(
        "SUP01", "Global Tech Supplies", "orders@globaltech.com"
    )

    while True:
        print("----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Create Customer Order")
        print("6. Save Inventory")
        print("7. Exit")
        print("8. Load Products from CSV")
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
        elif choice == "8":
            csv_path = (
                input(f"Enter CSV path (default: {CSV_FILENAME}): ").strip()
                or CSV_FILENAME
            )
            load_products(csv_path, inventory, default_supplier)
        else:
            print("Invalid selection. Please choose an option between 1 and 8.\n")


if __name__ == "__main__":
    main()