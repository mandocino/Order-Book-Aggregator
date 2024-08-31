class dataPacket:
    def __init__(self, quantity, name):
        self.quantity = float(quantity)
        self.name = name

    def getQuantity(self):
        return self.quantity

    def setQuantity(self, value):
        self.quantity = float(value)

    def getName(self):
        return self.name

    def setName(self, value):
        self.name = value
