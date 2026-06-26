# ByteBites UML Draft (First Pass)

​```mermaid
classDiagram
    class Customer {
        +String name
        +List~Order~ purchase_history
        +is_verified() bool
    }

    class MenuItem {
        +String name
        +float price
        +String category
        +int popularity_rating
    }

    class Menu {
        +List~MenuItem~ items
        +add_item(item: MenuItem)
        +filter_by_category(category: String) List~MenuItem~
        +sort_by_popularity() List~MenuItem~
    }

    class Order {
        +Customer customer
        +List~MenuItem~ selected_items
        +add_item(item: MenuItem)
        +calculate_total() float
    }

    Customer "1" --> "*" Order : places
    Order "*" --> "*" MenuItem : contains
    Menu "1" --> "*" MenuItem : holds
​```