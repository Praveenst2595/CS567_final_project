import datetime


class Product:
    def __init__(self, product_id, name, price, stock, category):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category

    def update_stock(self, quantity):
        if self.stock - quantity < 0:
            raise ValueError("Not enough stock available.")
        self.stock -= quantity

    def restock(self, quantity):
        if quantity < 0:
            raise ValueError("Cannot restock with negative quantity.")
        self.stock += quantity

    def apply_discount(self, percentage):
        if percentage < 0 or percentage > 100:
            raise ValueError("Invalid discount percentage.")
        self.price = round(self.price * (1 - percentage / 100), 2)

    def is_out_of_stock(self):
        return self.stock == 0

    def calculate_stock_value(self):
        return self.stock * self.price

    def is_on_sale(self):
        """Check if the product is on sale (price is discounted)."""
        return self.price < self.original_price if hasattr(self, 'original_price') else False

    def mark_as_featured(self):
        """Mark the product as featured."""
        self.is_featured = True
        return f"Product {self.name} is now marked as featured."


    def __str__(self):
        return (f"{self.name} (ID: {self.product_id}, Price: ${self.price}, Stock: {self.stock}, "
                f"Category: {self.category})")


class Customer:
    def __init__(self, customer_id, name, email, phone_number):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.purchase_history = []

    def add_purchase(self, order):
        self.purchase_history.append(order)

    def update_phone_number(self, new_phone):
        if not new_phone.isdigit() or len(new_phone) != 10:
            raise ValueError("Invalid phone number format.")
        self.phone_number = new_phone
        return f"Phone number for {self.name} updated to {new_phone}."
    def get_recent_purchases(self, limit=5):
        sorted_history = sorted(self.purchase_history, key=lambda order: order.order_date, reverse=True)
        return sorted_history[:limit]

    def deactivate_account(self):
        self.is_active = False
        return f"Customer {self.name}'s account has been deactivated."


    def get_total_spent(self):
        return sum(order.total_cost for order in self.purchase_history)

    def get_loyalty_status(self):
        total_spent = self.get_total_spent()
        if total_spent > 5000:
            return "Platinum"
        elif total_spent > 2000:
            return "Gold"
        elif total_spent > 1000:
            return "Silver"
        return "Bronze"

    def has_purchased_product(self, product_id):
        """Check if the customer has purchased a specific product."""
        return any(product_id in [item['product'].product_id for item in order.items]
                   for order in self.purchase_history)

    def __str__(self):
        return (f"{self.name} (ID: {self.customer_id}, Email: {self.email}, "
                f"Phone: {self.phone_number}, Loyalty: {self.get_loyalty_status()})")


class Order:
    def __init__(self, order_id, customer, order_date):
        self.order_id = order_id
        self.customer = customer
        self.order_date = order_date
        self.items = []
        self.total_cost = 0

    def add_item(self, product, quantity):
        if product.stock < quantity:
            raise ValueError(f"Not enough stock for product {product.name}.")
        product.update_stock(quantity)
        self.items.append({"product": product, "quantity": quantity})
        self.total_cost += product.price * quantity

    def get_itemized_bill(self):
        bill = "\n".join(
            [f"{item['quantity']}x {item['product'].name} @ ${item['product'].price} each"
             for item in self.items]
        )
        return f"Order {self.order_id}:\n{bill}\nTotal: ${self.total_cost}"

    def calculate_estimated_delivery_date(self, shipping_days=5):
        return self.order_date + datetime.timedelta(days=shipping_days)

    def add_gift_message(self, message):
        self.gift_message = message
        return f"Gift message added: {message}"

    def apply_order_discount(self, percentage):
        if percentage < 0 or percentage > 100:
            raise ValueError("Invalid discount percentage.")
        self.total_cost = round(self.total_cost * (1 - percentage / 100), 2)

    def contains_product(self, product_id):
        return any(item['product'].product_id == product_id for item in self.items)

    def get_order_summary(self):
        """Get a summary of the order, including customer and total cost."""
        return (f"Order Summary:\n"
                f"Customer: {self.customer.name} ({self.customer.customer_id})\n"
                f"Order Date: {self.order_date}\n"
                f"Total Items: {len(self.items)}\n"
                f"Total Cost: ${self.total_cost}")


    def __str__(self):
        items_str = ", ".join(
            [f"{item['quantity']}x {item['product'].name}" for item in self.items]
        )
        return f"Order {self.order_id}: {items_str}, Total: ${self.total_cost}"


class ECommerce:
    def __init__(self):
        self.products = []
        self.customers = []
        self.orders = []

    # Product Management
    def add_product(self, product_id, name, price, stock, category):
        self.products.append(Product(product_id, name, price, stock, category))

    def list_products(self):
        return [str(product) for product in self.products]

    def restock_product(self, product_id, quantity):
        product = next((p for p in self.products if p.product_id == product_id), None)
        if not product:
            raise ValueError("Product not found.")
        product.restock(quantity)
        return f"{quantity} units added to {product.name}."

    def search_products_by_category(self, category):
        results = [product for product in self.products if product.category.lower() == category.lower()]
        return results if results else f"No products found in category '{category}'."

    def apply_discount_to_category(self, category, percentage):
        discounted_products = []
        for product in self.products:
            if product.category.lower() == category.lower():
                product.apply_discount(percentage)
                discounted_products.append(product)
        if not discounted_products:
            raise ValueError(f"No products found in category '{category}'.")
        return f"Discount applied to {len(discounted_products)} product(s) in category '{category}'."

    def list_out_of_stock_products(self):
        """List all products that are out of stock."""
        out_of_stock = [product for product in self.products if product.is_out_of_stock()]
        return out_of_stock if out_of_stock else "No out-of-stock products found."

    # Customer Management
    def add_customer(self, customer_id, name, email, phone_number):
        self.customers.append(Customer(customer_id, name, email, phone_number))

    def list_customers(self):
        return [str(customer) for customer in self.customers]

    def update_customer_email(self, customer_id, new_email):
        customer = next((c for c in self.customers if c.customer_id == customer_id), None)
        if not customer:
            raise ValueError("Customer not found.")
        customer.email = new_email
        return f"Email for {customer.name} updated to {new_email}."

    def get_customers_by_loyalty(self, loyalty_level):
        return [customer for customer in self.customers if customer.get_loyalty_status().lower() == loyalty_level.lower()]

    def find_customers_purchased_product(self, product_id):
        """Find all customers who have purchased a specific product."""
        return [customer for customer in self.customers if customer.has_purchased_product(product_id)]

    # Order Management
    def place_order(self, order_id, customer_id, items):
        customer = next((c for c in self.customers if c.customer_id == customer_id), None)
        if not customer:
            raise ValueError("Customer not found.")

        order = Order(order_id, customer, datetime.date.today())
        for product_id, quantity in items.items():
            product = next((p for p in self.products if p.product_id == product_id), None)
            if not product:
                raise ValueError(f"Product {product_id} not found.")
            order.add_item(product, quantity)

        customer.add_purchase(order)
        self.orders.append(order)

    def list_orders(self):
        return [str(order) for order in self.orders]

    def get_orders_in_date_range(self, start_date, end_date):
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        orders_in_range = [order for order in self.orders if start_date <= order.order_date <= end_date]
        return orders_in_range if orders_in_range else "No orders found in the given date range."

    def cancel_order(self, order_id):
        order = next((o for o in self.orders if o.order_id == order_id), None)
        if not order:
            raise ValueError("Order not found.")
        for item in order.items:
            item["product"].stock += item["quantity"]
        self.orders.remove(order)
        return f"Order {order_id} has been canceled and stock returned."

    # Reports and Analytics
    def generate_sales_report(self):
        total_sales = sum(order.total_cost for order in self.orders)
        return f"Total Sales: ${total_sales}"

    def customer_purchase_history(self, customer_id):
        customer = next((c for c in self.customers if c.customer_id == customer_id), None)
        if not customer:
            return "Customer not found."
        history = "\n".join(order.get_itemized_bill() for order in customer.purchase_history)
        return f"Purchase History for {customer.name}:\n{history}" if history else "No purchases found."

    def calculate_total_inventory_value(self):
        return sum(product.calculate_stock_value() for product in self.products)

    def get_featured_products(self):
        featured_products = [product for product in self.products if getattr(product, 'is_featured', False)]
        return featured_products if featured_products else "No featured products available."

    def get_inactive_customers(self):
        return [customer for customer in self.customers if not getattr(customer, 'is_active', True)]

    def get_highest_spending_customer(self):
        if not self.customers:
            return "No customers available."
        highest_spender = max(self.customers, key=lambda c: c.get_total_spent(), default=None)
        return highest_spender if highest_spender else "No purchases yet."

    def get_orders_by_customer(self, customer_id):
        customer_orders = [order for order in self.orders if order.customer.customer_id == customer_id]
        return customer_orders if customer_orders else f"No orders found for customer ID {customer_id}."


    def calculate_total_inventory_value(self):
        return sum(product.calculate_stock_value() for product in self.products)

    def find_top_selling_product(self):
        product_sales = {}
        for order in self.orders:
            for item in order.items:
                product = item['product']
                product_sales[product.product_id] = product_sales.get(product.product_id, 0) + item['quantity']
        if not product_sales:
            return "No sales data available."
        top_product_id = max(product_sales, key=product_sales.get)
        top_product = next((p for p in self.products if p.product_id == top_product_id), None)
        return f"Top Selling Product: {top_product.name} (Sold: {product_sales[top_product_id]} units)" if top_product else "No products found."

    def find_customers_with_high_spending(self, threshold):
        return [customer for customer in self.customers if customer.get_total_spent() > threshold]

    def find_orders_by_date(self, date_str):
        target_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        return [order for order in self.orders if order.order_date == target_date]


    def find_most_purchased_product(self):
        product_counts = {}
        for order in self.orders:
            for item in order.items:
                product_id = item['product'].product_id
                product_counts[product_id] = product_counts.get(product_id, 0) + item['quantity']
        if not product_counts:
            return "No products have been purchased yet."
        most_purchased_id = max(product_counts, key=product_counts.get)
        most_purchased = next((p for p in self.products if p.product_id == most_purchased_id), None)
        return most_purchased if most_purchased else "Error finding the most purchased product."

    def generate_customer_spending_report(self):
        customer_spending = {}
        for customer in self.customers:
            total_spent = sum(order.total_cost for order in self.orders if order.customer == customer)
            customer_spending[customer.name] = total_spent

        report = "Customer Spending Report:\n"
        report += "\n".join([f"{name}: ${amount:.2f}" for name, amount in sorted(customer_spending.items(), key=lambda x: x[1], reverse=True)])

        return report

    def generate_customer_order_history(self, customer_id):
        customer = next((c for c in self.customers if c.customer_id == customer_id), None)
        if not customer:
            return f"No customer found with ID {customer_id}."

        customer_orders = [order for order in self.orders if order.customer == customer]

        if not customer_orders:
            return f"No orders found for customer {customer.name}."

        report = f"Order History for {customer.name} (ID: {customer.customer_id}):\n\n"

        for order in customer_orders:
            items_summary = ", ".join([f"{item['quantity']}x {item['product'].name}" for item in order.items])
            report += (
                f"Order ID: {order.order_id}\n"
                f"Date: {order.order_date}\n"
                f"Total: ${order.total_cost:.2f}\n"
                f"Items: {items_summary}\n\n"
            )

        return report

