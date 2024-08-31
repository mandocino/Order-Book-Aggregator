class Data:
    def __init__(self, price, quantity, name):
        self.price = float(price)
        self.quantity = float(quantity)
        self.name = name

    def price(self):
        return self._price

    def price(self, value):
        self._price = float(value)

    def quantity(self):
        return self._quantity

    def quantity(self, value):
        self._quantity = float(value)
