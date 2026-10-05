# ByteBites Backend Models
# Classes: Customer, MenuItem, Menu, Order


class MenuItem:
    """A single food item on the menu."""
    def __init__(self, name, price, category, popularity_rating):
        self.name = name
        self.price = price
        self.category = category
        self.popularity_rating = popularity_rating

    def __repr__(self):
        return f"MenuItem({self.name}, ${self.price}, {self.category})"


class Menu:
    """Manages the full collection of menu items."""
    def __init__(self):
        self.items = []

    def add_item(self, item):
        """Add a MenuItem to the menu."""
        self.items.append(item)

    def filter_by_category(self, category):
        """Return items matching the given category."""
        return [item for item in self.items if item.category.lower() == category.lower()]

    def sort_by_popularity(self):
        """Return items sorted by popularity (highest first)."""
        return sorted(self.items, key=lambda item: item.popularity_rating, reverse=True)


class Order:
    """A single transaction grouping selected items."""
    def __init__(self):
        self.selected_items = []

    def add_item(self, item):
        """Add a MenuItem to this order."""
        self.selected_items.append(item)

    def calculate_total(self):
        """Compute the total cost of all selected items."""
        return sum(item.price for item in self.selected_items)


class Customer:
    """A customer with name and purchase history."""
    def __init__(self, name):
        self.name = name
        self.purchase_history = []

    def place_order(self, order):
        """Record a completed order in purchase history."""
        self.purchase_history.append(order)

    def is_verified(self):
        """A customer is verified if they have at least one past order."""
        return len(self.purchase_history) > 0