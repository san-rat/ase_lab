import pytest
from src.catalog import Product, Catalog
from src.cart import Cart


class FakeInventory:
    """A fake inventory service for testing."""
    def __init__(self, stock):
        self._stock = stock

    def get_available(self, sku):
        return self._stock.get(sku, 0)


class TestInventoryReservation:
    def setup_method(self):
        self.catalog = Catalog()
        self.catalog.add_product(Product("SKU001", "Laptop", 1000.0))
        self.catalog.add_product(Product("SKU002", "Mouse", 25.0))

    def test_add_item_within_stock(self):
        inventory = FakeInventory({"SKU001": 5, "SKU002": 10})
        cart = Cart(self.catalog, inventory)
        cart.add_item("SKU001", 3)
        assert cart.total() == 3000.0

    def test_add_item_exceeding_stock_raises_error(self):
        inventory = FakeInventory({"SKU001": 2})
        cart = Cart(self.catalog, inventory)
        with pytest.raises(ValueError):
            cart.add_item("SKU001", 5)

    def test_add_item_with_zero_stock_raises_error(self):
        inventory = FakeInventory({"SKU001": 0})
        cart = Cart(self.catalog, inventory)
        with pytest.raises(ValueError):
            cart.add_item("SKU001", 1)
