import pytest
from src.catalog import Product, Catalog
from src.cart import Cart
from src.discount import DiscountEngine
from src.checkout import CheckoutService
from src.order import Order, OrderRepository


class FakePaymentGateway:
    def __init__(self, should_succeed=True):
        self._should_succeed = should_succeed

    def charge(self, amount, token):
        if not self._should_succeed:
            raise Exception("Payment declined")
        return True


class FakeOrderRepository(OrderRepository):
    def __init__(self):
        self._orders = []

    def save(self, order):
        self._orders.append(order)

    def get_all(self):
        return self._orders


class TestOrderHistory:
    def setup_method(self):
        self.catalog = Catalog()
        self.catalog.add_product(Product("SKU001", "Laptop", 500.0))
        self.cart = Cart(self.catalog)
        self.cart.add_item("SKU001", 2)

    def test_successful_checkout_creates_order(self):
        repo = FakeOrderRepository()
        gateway = FakePaymentGateway(should_succeed=True)
        engine = DiscountEngine([])
        checkout = CheckoutService(gateway, engine, repo)
        checkout.process(self.cart, "token123")
        orders = repo.get_all()
        assert len(orders) == 1
        assert orders[0].total == 1000.0

    def test_failed_checkout_does_not_create_order(self):
        repo = FakeOrderRepository()
        gateway = FakePaymentGateway(should_succeed=False)
        engine = DiscountEngine([])
        checkout = CheckoutService(gateway, engine, repo)
        checkout.process(self.cart, "token123")
        assert len(repo.get_all()) == 0

    def test_order_has_timestamp(self):
        repo = FakeOrderRepository()
        gateway = FakePaymentGateway(should_succeed=True)
        engine = DiscountEngine([])
        checkout = CheckoutService(gateway, engine, repo)
        checkout.process(self.cart, "token123")
        order = repo.get_all()[0]
        assert order.timestamp is not None
