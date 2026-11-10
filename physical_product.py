from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self._weight: float = float(weight)

    @property
    def weight(self) -> float:
        return self._weight

    def calculate_shipping_cost(self) -> float:
        return 5.00 + (self._weight * 2.50)

    def get_fulfilment_info(self) -> str:
        return f"Physical shipping required. Shipping cost: ${self.calculate_shipping_cost():.2f}"

    def display_information(self) -> None:
        super().display_information()
        print(f" | Weight: {self._weight:.2f} kg | Shipping: ${self.calculate_shipping_cost():.2f}")

    def to_dict(self) -> dict:
        return {
            "type": "physical",
            "name": self.name,
            "price": self._price,
            "stock": self._stock,
            "weight": self._weight,
            "supplier": self.supplier.to_dict()
        }