# ByteBites Final Design

​```mermaid
classDiagram
    class Customer {
        +str name
        +list purchase_history
        +is_verified() bool
    }

    class MenuItem {
        +str name
        +float price
        +str category
        +int popularity_rating
    }

    class Menu {
        +list items
        +add_item(item: MenuItem)
        +filter_by_category(category: str) list
        +sort_by_popularity() list
    }

    class Order {
        +list selected_items
        +add_item(item: MenuItem)
        +calculate_total() float
    }

    Customer "1" --> "*" Order : places
    Order "*" --> "*" MenuItem : contains
    Menu "1" --> "*" MenuItem : holds
​```

## Design Notes
- Customer tracks purchase history as a list of past Orders
- MenuItem is a simple data object with no complex behavior
- Menu manages the collection and provides filtering/sorting
- Order groups selected items and computes total cost
- No inheritance used — all relationships are composition (has-a)