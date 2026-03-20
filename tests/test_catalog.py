import pytest
from src.catalog import Product, Catalog


class TestProduct:
    def test_create_product_with_valid_data(self):
        product = Product("SKU001", "Laptop", 999.99)
        assert product.sku == "SKU001"
        assert product.name == "Laptop"
        assert product.price == 999.99

    def test_create_product_with_negative_price_raises_error(self):
        with pytest.raises(ValueError):
            Product("SKU002", "Bad Product", -10.0)

    def test_create_product_with_zero_price(self):
        product = Product("SKU003", "Free Item", 0)
        assert product.price == 0


class TestCatalog:
    def test_add_and_get_product(self):
        catalog = Catalog()
        product = Product("SKU001", "Laptop", 999.99)
        catalog.add_product(product)
        assert catalog.get_product("SKU001") == product

    def test_get_missing_product_returns_none(self):
        catalog = Catalog()
        assert catalog.get_product("MISSING") is None
