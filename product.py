from abc import ABC, abstractmethod
from supplier import Supplier


class Product(ABC):

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
    ) -> None:
        converted_price = float(price)
        converted_stock = int(stock)

        if converted_price <= 0:
            raise ValueError("Price must be greater than zero.")
        if converted_stock < 0:
            raise ValueError("Stock quantity cannot be negative.")

        self._product_id: str = product_id
        self.name: str = name
        self._price: float = converted_price
        self._stock: int = converted_stock
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
        converted_qty = int(quantity)
        if converted_qty < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self._stock = converted_qty

    def display_information(self) -> None:
        print(
            f"ID: {self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | "
            f"Stock: {self._stock} | Supplier: {self._supplier.name} ({self._supplier.contact_email})",
            end="",
        )

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass