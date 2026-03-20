class Cart:
    def __init__(self, catalog, inventory=None):
        self._catalog = catalog
        self._inventory = inventory
        self._items = {}

    def add_item(self, sku, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        if self._catalog.get_product(sku) is None:
            raise ValueError("Product not found in catalog")
        if self._inventory is not None:
            available = self._inventory.get_available(sku)
            if quantity > available:
                raise ValueError("Not enough stock available")
        self._items[sku] = quantity

    def remove_item(self, sku):
        del self._items[sku]

    def total(self):
        result = 0
        for sku, quantity in self._items.items():
            product = self._catalog.get_product(sku)
            result += product.price * quantity
        return result

    def get_items(self):
        items = {}
        for sku, quantity in self._items.items():
            product = self._catalog.get_product(sku)
            items[sku] = {"price": product.price, "quantity": quantity}
        return items

