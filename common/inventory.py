# MysteryIsland/common/inventory.py

class Inventory:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def has(self, item):
        return item in self.items


'''
class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        if item not in self.items:
            self.items.append(item)

    def has_item(self, item):
        return item in self.items

    def get_items(self):
        return self.items

    def clear(self):
        self.items.clear()
'''