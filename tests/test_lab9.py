import os
import tempfile
import unittest
from unittest.mock import patch

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product_factory import ProductFactory
from order_line import OrderLine
from order import Order
from inventory import Inventory
from discount_strategy import (
    NoDiscount,
    PercentageDiscount,
    BulkDiscount,
    StudentDiscount,
)
from inventory_manager_OOP import get_positive_float, load_products


class TestLab9(unittest.TestCase):

    def setUp(self) -> None:
        self.supplier = Supplier("SUP01", "Test Supplier", "test@supplier.com")
        self.lamp = ProductFactory.create(
            "physical", "P001", "Desk Lamp", 50.0, 10, self.supplier
        )
        self.editor = ProductFactory.create(
            "digital", "D001", "Photo Editor", 100.0, 20, self.supplier
        )

    def test_order_default_no_discount(self) -> None:
        order = Order("ORD01")
        order.add_order_line(self.lamp, 2)  # 100.0
        self.assertAlmostEqual(order.calculate_total(), 100.0)

    def test_order_bulk_and_percentage_discount_switching(self) -> None:
        order = Order("ORD02", BulkDiscount(200, 20))
        order.add_order_line(self.lamp, 1)    # 50.0
        order.add_order_line(self.editor, 2)  # 200.0 -> Subtotal = 250.0
        self.assertAlmostEqual(order.calculate_total(), 230.0)

        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

    def test_order_student_discount(self) -> None:
        order = Order("ORD03", StudentDiscount())
        order.add_order_line(self.editor, 2)  # 200.0
        self.assertAlmostEqual(order.calculate_total(), 190.0)

    def test_product_factory_creates_correct_subclasses(self) -> None:
        self.assertIsInstance(self.lamp, PhysicalProduct)
        self.assertIsInstance(self.lamp, Product)
        self.assertIsInstance(self.editor, DigitalProduct)
        self.assertIsInstance(self.editor, Product)

    def test_product_factory_unknown_type_raises_value_error(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            ProductFactory.create(
                "service", "S001", "Installation", 30.0, 5, self.supplier
            )
        self.assertIn("Unknown product type", str(ctx.exception))

    def test_invalid_product_price_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create(
                "physical", "Pbad", "Bad Price", 0, 5, self.supplier
            )
        with self.assertRaises(ValueError):
            ProductFactory.create(
                "physical", "Pbad2", "Negative Price", -10.0, 5, self.supplier
            )

    def test_invalid_stock_quantity_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create(
                "physical", "Pbad3", "Negative Stock", 10.0, -1, self.supplier
            )
        with self.assertRaises(ValueError):
            self.lamp.update_stock(-5)

    def test_invalid_order_line_quantity_rejected(self) -> None:
        with self.assertRaises(ValueError):
            OrderLine(self.lamp, 0)
        with self.assertRaises(ValueError):
            OrderLine(self.lamp, -3)

    @patch("builtins.input", side_effect=["abc", "-5", "12.50"])
    def test_get_positive_float_retries_on_invalid_input(
        self, mock_input: unittest.mock.MagicMock
    ) -> None:
        result = get_positive_float("Enter price: ")
        self.assertAlmostEqual(result, 12.50)
        self.assertEqual(mock_input.call_count, 3)


    def test_load_products_missing_file_handled_gracefully(self) -> None:
        inv = Inventory()
        # Should not raise FileNotFoundError
        load_products("non_existent_file_12345.csv", inv, self.supplier)
        self.assertEqual(len(inv.products), 0)

    def test_load_products_skips_bad_rows_and_loads_valid_rows(self) -> None:
        csv_content = (
            "product_type,product_id,name,price,stock_quantity\n"
            "physical,P001,Desk Lamp,25.00,10\n"
            "digital,D001,Photo Editor,49.90,100\n"
            "service,S001,Installation,30.00,5\n"
            "physical,P002,Office Chair,abc,3\n"
            "physical,P003,Monitor Stand,39.50,7\n"
        )
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".csv", newline=""
        ) as tmp:
            tmp.write(csv_content)
            tmp_path = tmp.name

        try:
            inv = Inventory()
            load_products(tmp_path, inv, self.supplier)
            self.assertEqual(len(inv.products), 3)
            self.assertIsNotNone(inv.find_product("P001"))
            self.assertIsNotNone(inv.find_product("D001"))
            self.assertIsNotNone(inv.find_product("P003"))
            self.assertIsNone(inv.find_product("S001"))
            self.assertIsNone(inv.find_product("P002"))
        finally:
            os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()