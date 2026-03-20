import pytest
from src.catalog import Product, Catalog
from src.cart import Cart
from src.discount import BulkDiscount, OrderDiscount, DiscountEngine
from src.checkout import CheckoutService


class FakePaymentGateway:
    def __init__(self, should_succeed=True):
        self._should_succeed = should_succeed
        self.charged_amount = None

    def charge(self, amount, token):
        if not self._should_succeed:
            raise Exception("Payment declined")
        self.charged_amount = amount
        return True


class TestCheckout:
    def setup_method(self):
        self.catalog = Catalog()
        self.catalog.add_product(Product("SKU001", "Laptop", 500.0))
        self.cart = Cart(self.catalog)
        self.cart.add_item("SKU001", 2)

    def test_successful_checkout(self):
        gateway = FakePaymentGateway(should_succeed=True)
        engine = DiscountEngine([])
        checkout = CheckoutService(gateway, engine)
        result = checkout.process(self.cart, "token123")
        assert result["success"] is True
        assert gateway.charged_amount == 1000.0

    def test_checkout_with_discount(self):
        gateway = FakePaymentGateway(should_succeed=True)
        engine = DiscountEngine([OrderDiscount()])
        checkout = CheckoutService(gateway, engine)
        result = checkout.process(self.cart, "token123")
        assert result["success"] is True
        assert gateway.charged_amount == 950.0

    def test_checkout_payment_failure(self):
        gateway = FakePaymentGateway(should_succeed=False)
        engine = DiscountEngine([])
        checkout = CheckoutService(gateway, engine)
        result = checkout.process(self.cart, "token123")
        assert result["success"] is False
        assert "error" in result
