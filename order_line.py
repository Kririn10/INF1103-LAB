from product import Product


class OrderLine:
    """Represents one product and quantity inside an order (Composition part of Order)."""

    def __init__(self, product: Product, quantity: int) -> None:
        self.product: Product = product
        self.quantity: int = int(quantity)

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

    def display_line(self) -> None:
        print(f"  - {self.product.name} (x{self.quantity}) @ ${self.product.price:.2f} each = ${self.calculate_subtotal():.2f}")