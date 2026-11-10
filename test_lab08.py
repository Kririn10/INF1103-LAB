from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from product import Product


def test_lsp_and_polymorphism(product: Product) -> None:

    print(f"Testing LSP with: {product.__class__.__name__}")
    product.display_information()
    print()
    print(f"Fulfilment Info : {product.get_fulfilment_info()}")
    print("-" * 60)


def main() -> None:
    print("=" * 60)
    print("LAB 8: OOP concept tester")
    print("=" * 60)

    # 1. Association: Supplier and Product
    print("\n--- 1. Testing Association (Supplier & Product) ---")
    sup = Supplier("SUP01", "Nexus Electronics", "support@nexuselec.com")
    laptop = PhysicalProduct("P001", "UltraBook", 1450.00, 10, 1.8, sup)
    ebook = DigitalProduct("D001", "Python Guide", 29.99, 100, 45.0, sup)

    print("Product referencing Supplier:")
    laptop.display_information()
    print()

    # Test independent existence
    del sup
    print("Supplier deleted from local scope. Verifying Product still holds reference:")
    print(f"Supplier Name via Product: {laptop.supplier.name} ({laptop.supplier.contact_email})")

    # 2. Aggregation: Inventory and Product
    print("\n--- 2. Testing Aggregation (Inventory & Product) ---")
    inv_a = Inventory()
    inv_b = Inventory()

    inv_a.add_product(laptop)
    inv_a.add_product(ebook)
    print(f"Inventory A count: {len(inv_a.products)}")

    # Remove laptop from Inventory A and transfer to Inventory B
    removed_product = inv_a.remove_product("P001")
    print(f"Removed '{removed_product.name}' from Inventory A. Inventory A count: {len(inv_a.products)}")
    print(f"Confirming product still alive outside inventory: {removed_product.name} (Stock: {removed_product.stock})")

    inv_b.add_product(removed_product)
    print(f"Added to Inventory B. Inventory B count: {len(inv_b.products)}")

    # 3. Composition: Order and OrderLine
    print("\n--- 3. Testing Composition (Order & OrderLine) ---")
    order1 = Order("ORD-101")
    order2 = Order("ORD-102")

    order1.add_order_line(laptop, 1)
    order2.add_order_line(laptop, 2)

    line1 = order1.order_lines[0]
    line2 = order2.order_lines[0]

    print(f"Order 1 Line ID: {id(line1)} | Order 2 Line ID: {id(line2)}")
    print(f"Are OrderLines distinct objects? {line1 is not line2}")
    print(f"Do both OrderLines reference the EXACT same Product? {line1.product is line2.product}")
    order1.display_order_summary()
    order2.display_order_summary()

    # 4. Polymorphism & Liskov Substitution Principle (LSP)
    print("--- 4. Testing LSP & Polymorphism via Product Reference ---")
    catalog: list[Product] = [laptop, ebook]
    for item in catalog:
        # Invokes specialized behavior through the common abstraction
        test_lsp_and_polymorphism(item)

    print("Test successful.")


if __name__ == "__main__":
    main()