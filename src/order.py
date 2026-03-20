from datetime import datetime


class Order:
    def __init__(self, items, total):
        self.items = items
        self.total = total
        self.timestamp = datetime.now()


class OrderRepository:
    def save(self, order):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError
