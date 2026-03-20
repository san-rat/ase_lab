class Product:
    def __init__(self, sku, name, price):
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.sku = sku
        self.name = name
        self.price = price


class Catalog:
    def __init__(self):
        self._products = {}

    def add_product(self, product):
        self._products[product.sku] = product

    def get_product(self, sku):
        return self._products.get(sku, None)
