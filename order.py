from product import Product
from order_line import OrderLine


class Order:

    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Creates OrderLine internally to enforce composition lifecycle ownership."""
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def display_order_summary(self) -> None:
        print(f"\nOrder ID: {self.order_id}")
        for line in self.order_lines:
            line.display_line()
        print(f"Total Amount: ${self.calculate_total():.2f}\n")