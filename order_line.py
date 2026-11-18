from product import Product


class OrderLine:

    def __init__(self, product: Product, quantity: int) -> None:
        converted_qty = int(quantity)
        if converted_qty <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.product: Product = product
        self.quantity: int = converted_qty

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

    def display_line(self) -> None:
        print(
            f"  - {self.product.name} (x{self.quantity}) @ ${self.product.price:.2f} each = ${self.calculate_subtotal():.2f}"
        )