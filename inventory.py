from product import Product


class Inventory:

    def __init__(self):
        self._products: dict[str, Product] = {}

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

    def get_all_products(self) -> dict[str, Product]:
        return self._products