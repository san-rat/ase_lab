class BulkDiscount:
    def calculate(self, items, subtotal):
        discount = 0
        for sku, info in items.items():
            if info["quantity"] >= 10:
                discount += info["price"] * info["quantity"] * 0.10
        return discount


class OrderDiscount:
    def calculate(self, items, subtotal):
        if subtotal >= 1000:
            return subtotal * 0.05
        return 0


class DiscountEngine:
    def __init__(self, rules):
        self._rules = rules

    def apply(self, cart):
        subtotal = cart.total()
        items = cart.get_items()
        total_discount = 0
        for rule in self._rules:
            total_discount += rule.calculate(items, subtotal)
        return subtotal - total_discount

