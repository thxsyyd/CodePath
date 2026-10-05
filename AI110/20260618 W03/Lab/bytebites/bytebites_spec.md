# Client Feature Request

We need to build the backend logic for the ByteBites app. The system needs to manage our customers, tracking their names and their past purchase history so the system can verify they are real users.

These customers need to browse specific food items (like a "Spicy Burger" or "Large Soda"), so we must track the name, price, category, and popularity rating for every item we sell.

We also need a way to manage the full collection of items — a digital list that holds all items and lets us filter by category such as "Drinks" or "Desserts".

Finally, when a user picks items, we need to group them into a single transaction. This transaction object should store the selected items and compute the total cost.

# Candidate Classes

1. **Customer** — 顾客，存储姓名和购买历史
2. **MenuItem** — 食品项，存储名称、价格、类别、人气评分
3. **Menu** — 菜单，管理所有食品项的集合，支持按类别筛选
4. **Order** — 订单/交易，存储用户选的食品项，计算总价