import pytest
from src.catalog import Product, Catalog
from src.cart import Cart
from src.discount import BulkDiscount, OrderDiscount, DiscountEngine


class TestBulkDiscount:
    def test_bulk_discount_applies_when_quantity_is_10_or_more(self):
        rule = BulkDiscount()
        # SKU001: price 100, quantity 10 => line total 1000, with 10% off => 900
        items = {"SKU001": {"price": 100.0, "quantity": 10}}
        discount = rule.calculate(items, 1000.0)
        assert discount == 100.0

    def test_bulk_discount_does_not_apply_below_10(self):
        rule = BulkDiscount()
        items = {"SKU001": {"price": 100.0, "quantity": 5}}
        discount = rule.calculate(items, 500.0)
        assert discount == 0


class TestOrderDiscount:
    def test_order_discount_applies_when_total_is_1000_or_more(self):
        rule = OrderDiscount()
        items = {}
        discount = rule.calculate(items, 1000.0)
        assert discount == 50.0

    def test_order_discount_does_not_apply_below_1000(self):
        rule = OrderDiscount()
        items = {}
        discount = rule.calculate(items, 999.0)
        assert discount == 0


class TestDiscountEngine:
    def setup_method(self):
        self.catalog = Catalog()
        self.catalog.add_product(Product("SKU001", "Laptop", 100.0))

    def test_engine_applies_all_rules(self):
        cart = Cart(self.catalog)
        cart.add_item("SKU001", 10)
        # Subtotal = 1000, bulk discount = 100, order discount = 50
        engine = DiscountEngine([BulkDiscount(), OrderDiscount()])
        final = engine.apply(cart)
        assert final == 850.0
