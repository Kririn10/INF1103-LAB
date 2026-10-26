import json
import os

FILENAME = "inventory.json"


class Product:

    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self._product_id = product_id
        self.name = name
        self._price = float(price)
        self._stock = int(stock)

    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def price(self) -> float:
        return self._price

    @property
    def stock(self) -> int:
        return self._stock

    def update_stock(self, quantity: int) -> None:
        if quantity < 0:
            print("Stock quantity cannot be negative.")
            return
        self._stock = quantity

    def display_information(self) -> None:
        print(f"ID: {self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | Stock: {self._stock}")

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "price": self._price,
            "stock": self._stock
        }


class Inventory:

    def __init__(self):
        self._products = {}

    def add_product(self, product: Product) -> bool:
        if product.product_id in self._products:
            print("A product with this ID already exists!\n")
            return False
        self._products[product.product_id] = product
        return True

    def search_product(self, product_id: str) -> Product | None:
        return self._products.get(product_id)

    def display_all(self) -> None:
        if not self._products:
            print("Inventory is currently empty.\n")
            return

        print("\nCurrent Inventory")
        for product in self._products.values():
            product.display_information()
        print()

    def get_all_products(self) -> dict:
        return self._products


def load_inventory() -> Inventory:
    inventory = Inventory()

    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                data = json.load(file)
                print("inventory.json found.")
                print("Inventory loaded successfully.\n")
                for pid, details in data.items():
                    product = Product(pid, details["name"], details["price"], details["stock"])
                    inventory.add_product(product)
                return inventory
        except (json.JSONDecodeError, IOError):
            print("Error loading inventory file. Starting with default inventory.\n")

    defaults = [
        Product("P001", "Laptop", 1200.00, 15),
        Product("P002", "Mouse", 25.50, 40),
        Product("P003", "Keyboard", 45.00, 25),
    ]
    for p in defaults:
        inventory.add_product(p)

    return inventory


def save_inventory(inventory: Inventory) -> None:
    print("Saving inventory...")
    data = {
        pid: prod.to_dict()
        for pid, prod in inventory.get_all_products().items()
    }
    try:
        with open(FILENAME, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Inventory saved successfully to {FILENAME}.\n")
    except IOError as e:
        print(f"Failed to save inventory: {e}\n")



def prompt_add_product(inventory: Inventory) -> None:
    print("\nAdd New Product")
    pid = input("Product ID: ").strip()
    if inventory.search_product(pid):
        print("A product with this ID already exists!\n")
        return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())
    except ValueError:
        print("Invalid price or stock quantity. Operation aborted.\n")
        return

    product = Product(pid, name, price, stock)
    if inventory.add_product(product):
        print("Product added successfully!\n")


def prompt_update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    pid = input("Enter Product ID: ").strip()
    product = inventory.search_product(pid)

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
    product = inventory.search_product(pid)

    if product:
        print("Product Found")
        print("-" * 40)
        print(f"ID: {product.product_id}\nName: {product.name}\nPrice: ${product.price:.2f}\nStock: {product.stock}")
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
            inventory.display_all()
        elif choice == "2":
            prompt_add_product(inventory)
        elif choice == "3":
            prompt_update_stock(inventory)
        elif choice == "4":
            prompt_search_product(inventory)
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