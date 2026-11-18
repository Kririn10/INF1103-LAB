import json
import os
from product import Product
from product_factory import ProductFactory
from supplier import Supplier


class Inventory:

    def __init__(self) -> None:
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

    def display_all(self) -> None:
        if not self.products:
            print("Inventory is currently empty.\n")
            return

        print("\nCurrent Inventory:")
        for product in self.products:
            product.display_information()
        print()

    def save_to_file(self, filename: str = "inventory.json") -> None:
        print("Saving inventory...")
        data = {
            product.product_id: product.to_dict() for product in self.products
        }
        try:
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)
            print(f"Inventory saved successfully to {filename}.\n")
        except IOError as e:
            print(f"Failed to save inventory: {e}\n")

    def load_from_file(self, filename: str = "inventory.json") -> None:
        default_supplier = Supplier(
            "SUP01", "Global Tech Supplies", "orders@globaltech.com"
        )

        if os.path.exists(filename):
            try:
                with open(filename, "r") as file:
                    data = json.load(file)
                    print(f"{filename} found.")
                    print("Inventory loaded successfully.\n")
                    self.products.clear()
                    for pid, details in data.items():
                        supp_data = details.get("supplier")
                        if supp_data and isinstance(supp_data, dict):
                            prod_supplier = Supplier(
                                supp_data.get("supplier_id", "SUP01"),
                                supp_data.get("name", "Global Tech Supplies"),
                                supp_data.get(
                                    "contact_email", "orders@globaltech.com"
                                ),
                            )
                        else:
                            prod_supplier = default_supplier

                        prod_type = details.get("type", "physical")
                        product = ProductFactory.create(
                            prod_type,
                            pid,
                            details["name"],
                            details["price"],
                            details["stock"],
                            prod_supplier,
                            weight=details.get("weight", 1.0),
                            download_size=details.get("download_size", 100.0),
                        )
                        self.add_product(product)
                    return
            except (json.JSONDecodeError, IOError, ValueError):
                print(f"Error loading {filename}. Loading defaults.\n")

        # Fallback defaults created via ProductFactory
        self.products.clear()
        defaults = [
            ProductFactory.create(
                "physical", "P001", "Laptop", 1200.00, 15, default_supplier, weight=2.3
            ),
            ProductFactory.create(
                "physical", "P002", "Mouse", 25.50, 40, default_supplier, weight=0.15
            ),
            ProductFactory.create(
                "digital",
                "P003",
                "Antivirus Suite",
                45.00,
                100,
                default_supplier,
                download_size=350.0,
            ),
        ]
        for p in defaults:
            self.add_product(p)