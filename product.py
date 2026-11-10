from abc import ABC, abstractmethod
from supplier import Supplier


class Product(ABC):
    """Abstract base class representing common product attributes and behaviors."""

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier) -> None:
        self._product_id: str = product_id
        self.name: str = name
        self._price: float = float(price)
        self._stock: int = int(stock)
        self._supplier: Supplier = supplier

    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def price(self) -> float:
        return self._price

    @property
    def stock(self) -> int:
        return self._stock

    @property
    def supplier(self) -> Supplier:
        return self._supplier

    def update_stock(self, quantity: int) -> None:
        if quantity < 0:
            print("Stock quantity cannot be negative.")
            return
        self._stock = quantity

    def display_information(self) -> None:
        """Display base product details and supplier info."""
        print(
            f"ID: {self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | "
            f"Stock: {self._stock} | Supplier: {self._supplier.name} ({self._supplier.contact_email})",
            end=""
        )

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return fulfillment details."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Serialize product data to dictionary."""
        pass