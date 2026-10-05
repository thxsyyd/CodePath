from models import MenuItem, Menu, Order, Customer


def test_calculate_total_with_multiple_items():
    order = Order()
    order.add_item(MenuItem("Spicy Burger", 8.99, "Entrees", 5))
    order.add_item(MenuItem("Large Soda", 2.49, "Drinks", 3))
    assert order.calculate_total() == 11.48


def test_order_total_is_zero_when_empty():
    order = Order()
    assert order.calculate_total() == 0


def test_filter_by_category():
    menu = Menu()
    menu.add_item(MenuItem("Burger", 8.99, "Entrees", 5))
    menu.add_item(MenuItem("Soda", 2.49, "Drinks", 3))
    menu.add_item(MenuItem("Water", 1.00, "Drinks", 2))
    result = menu.filter_by_category("Drinks")
    assert len(result) == 2


def test_filter_case_insensitive():
    menu = Menu()
    menu.add_item(MenuItem("Soda", 2.49, "Drinks", 3))
    assert len(menu.filter_by_category("drinks")) == 1


def test_sort_by_popularity():
    menu = Menu()
    menu.add_item(MenuItem("Soda", 2.49, "Drinks", 3))
    menu.add_item(MenuItem("Burger", 8.99, "Entrees", 5))
    sorted_items = menu.sort_by_popularity()
    assert sorted_items[0].name == "Burger"


def test_customer_not_verified_initially():
    assert Customer("Alice").is_verified() == False


def test_customer_verified_after_order():
    c = Customer("Alice")
    order = Order()
    order.add_item(MenuItem("Burger", 8.99, "Entrees", 5))
    c.place_order(order)
    assert c.is_verified() == True