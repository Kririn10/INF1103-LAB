from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self._download_size: float = float(download_size)

    @property
    def download_size(self) -> float:
        return self._download_size

    def get_fulfilment_info(self) -> str:
        return f"Delivered digitally via download link ({self._download_size:.2f} MB)."

    def display_information(self) -> None:
        super().display_information()
        print(f" | Download Size: {self._download_size:.2f} MB | Fulfilment: Delivered digitally")

    def to_dict(self) -> dict:
        return {
            "type": "digital",
            "name": self.name,
            "price": self._price,
            "stock": self._stock,
            "download_size": self._download_size,
            "supplier": self.supplier.to_dict()
        }