class CheckoutService:
    def __init__(self, payment_gateway, discount_engine):
        self._gateway = payment_gateway
        self._engine = discount_engine

    def process(self, cart, token):
        final_total = self._engine.apply(cart)
        try:
            self._gateway.charge(final_total, token)
            return {"success": True, "total": final_total}
        except Exception as e:
            return {"success": False, "error": str(e)}
