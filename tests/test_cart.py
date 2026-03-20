import pytest
from src.catalog import Product, Catalog
from src.cart import Cart


class TestCart:
    def setup_method(self):
        """Set up a catalog with some products for each test."""
        self.catalog = Catalog()
        self.catalog.add_product(Product("SKU001", "Laptop", 1000.0))
        self.catalog.add_product(Product("SKU002", "Mouse", 25.0))

    def test_add_item_and_get_total(self):
        cart = Cart(self.catalog)
        cart.add_item("SKU001", 2)
        assert cart.total() == 2000.0

    def test_add_multiple_items(self):
        cart = Cart(self.catalog)
        cart.add_item("SKU001", 1)
        cart.add_item("SKU002", 3)
        assert cart.total() == 1075.0

    def test_remove_item(self):
        cart = Cart(self.catalog)
        cart.add_item("SKU001", 2)
        cart.add_item("SKU002", 1)
        cart.remove_item("SKU001")
        assert cart.total() == 25.0

    def test_add_item_not_in_catalog_raises_error(self):
        cart = Cart(self.catalog)
        with pytest.raises(ValueError):
            cart.add_item("FAKE", 1)

    def test_add_item_with_zero_quantity_raises_error(self):
        cart = Cart(self.catalog)
        with pytest.raises(ValueError):
            cart.add_item("SKU001", 0)

    def test_add_item_with_negative_quantity_raises_error(self):
        cart = Cart(self.catalog)
        with pytest.raises(ValueError):
            cart.add_item("SKU001", -1)