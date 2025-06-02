# MysteryIsland/common/inventory.py

class Inventory:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def has(self, item):
        return item in self.items