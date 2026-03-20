from src.order import Order


class CheckoutService:
    def __init__(self, payment_gateway, discount_engine, order_repo=None):
        self._gateway = payment_gateway
        self._engine = discount_engine
        self._repo = order_repo

    def process(self, cart, token):
        final_total = self._engine.apply(cart)
        try:
            self._gateway.charge(final_total, token)
            if self._repo is not None:
                order = Order(cart.get_items(), final_total)
                self._repo.save(order)
            return {"success": True, "total": final_total}
        except Exception as e:
            return {"success": False, "error": str(e)}
