import json
import os
from product import Product


class Inventory:

    def __init__(self) -> None:
        # Lab 8 Section 3: Collection typed using the base class Product
        self.products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.product_id) is not None:
            print("A product with this ID already exists!\n")
            return False
        self.products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product:
            self.products.remove(product)
            return product
        return None

    def find_product(self, product_id: str) -> Product | None:
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None

    def search_product(self, product_id: str) -> Product | None:
        return self.find_product(product_id)

    def display_all(self) -> None:
        if not self.products:
            print("Inventory is currently empty.\n")
            return

        print("\nCurrent Inventory")
        for product in self.products:
            product.display_information()
        print()

    def save_to_file(self, filename: str = "inventory.json") -> None:
        print("Saving inventory...")
        data = {
            product.product_id: product.to_dict()
            for product in self.products
        }
        try:
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)
            print(f"Inventory saved successfully to {filename}.\n")
        except IOError as e:
            print(f"Failed to save inventory: {e}\n")

    def load_from_file(self, filename: str = "inventory.json") -> None:
        from physical_product import PhysicalProduct
        from digital_product import DigitalProduct

        if os.path.exists(filename):
            try:
                with open(filename, "r") as file:
                    data = json.load(file)
                    print(f"{filename} found.")
                    print("Inventory loaded successfully.\n")
                    self.products.clear()
                    for pid, details in data.items():
                        prod_type = details.get("type", "physical")
                        if prod_type == "digital":
                            product = DigitalProduct(
                                pid,
                                details["name"],
                                details["price"],
                                details["stock"],
                                details["download_size"]
                            )
                        else:
                            product = PhysicalProduct(
                                pid,
                                details["name"],
                                details["price"],
                                details["stock"],
                                details.get("weight", 1.0)
                            )
                        self.add_product(product)  
                    return
            except (json.JSONDecodeError, IOError):
                print(f"Error loading {filename}. Starting with default inventory.\n")

        # Fallback defaults if file does not exist or fails to load
        defaults = [
            PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.3),
            PhysicalProduct("P002", "Mouse", 25.50, 40, 0.15),
            DigitalProduct("P003", "Antivirus Suite", 45.00, 100, 350.0),
        ]
        self.products.clear()
        for p in defaults:
            self.add_product(p)