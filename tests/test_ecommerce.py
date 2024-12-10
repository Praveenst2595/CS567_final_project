import unittest
import datetime
from ecommerce.ecommerce import Product, Customer, Order, ECommerce


class TestECommerce(unittest.TestCase):

    def setUp(self):
        self.ecommerce = ECommerce()

        # Add sample products
        self.ecommerce.add_product("P001", "Laptop", 1000, 10, "Electronics")
        self.ecommerce.add_product("P002", "Phone", 500, 20, "Electronics")
        self.ecommerce.add_product("P003", "Table", 150, 5, "Furniture")

        # Add sample customers
        self.ecommerce.add_customer("C001", "Alice", "alice@example.com", "1234567890")
        self.ecommerce.add_customer("C002", "Bob", "bob@example.com", "9876543210")

        # Place sample orders
        self.ecommerce.place_order("O001", "C001", {"P001": 1, "P002": 2})
        self.ecommerce.place_order("O002", "C002", {"P003": 3})

    # === Product Tests ===
    def test_add_product(self):
        self.ecommerce.add_product("P004", "Chair", 100, 15, "Furniture")
        products = self.ecommerce.list_products()
        self.assertEqual(len(products), 4)
        self.assertIn("Chair", products[-1])

    def test_restock_product(self):
        response = self.ecommerce.restock_product("P001", 5)
        product = next(p for p in self.ecommerce.products if p.product_id == "P001")
        self.assertEqual(product.stock, 14)
        self.assertIn("5 units added", response)

    def test_apply_discount_to_category(self):
        response = self.ecommerce.apply_discount_to_category("Electronics", 10)
        product = next(p for p in self.ecommerce.products if p.product_id == "P001")
        self.assertEqual(product.price, 900)
        self.assertIn("Discount applied", response)

    def test_list_out_of_stock_products(self):
        self.ecommerce.products[0].stock = 0
        out_of_stock = self.ecommerce.list_out_of_stock_products()
        self.assertEqual(len(out_of_stock), 1)
        self.assertEqual(out_of_stock[0].name, "Laptop")

    # === Customer Tests ===
    def test_add_customer(self):
        self.ecommerce.add_customer("C003", "Charlie", "charlie@example.com", "5555555555")
        customers = self.ecommerce.list_customers()
        self.assertEqual(len(customers), 3)
        self.assertIn("Charlie", customers[-1])

    def test_update_phone_number(self):
        customer = next(c for c in self.ecommerce.customers if c.customer_id == "C001")
        response = customer.update_phone_number("5555555555")
        self.assertEqual(customer.phone_number, "5555555555")
        self.assertIn("Phone number for Alice updated", response)

    def test_get_recent_purchases(self):
        customer = next(c for c in self.ecommerce.customers if c.customer_id == "C001")
        self.ecommerce.place_order("O003", "C001", {"P003": 1})
        self.ecommerce.place_order("O004", "C001", {"P001": 2})
        recent_purchases = customer.get_recent_purchases(limit=2)
        self.assertEqual(len(recent_purchases), 2)
        self.assertEqual(recent_purchases[0].order_id, "O001")

    # === Order Tests ===
    def test_place_order(self):
        self.ecommerce.place_order("O003", "C001", {"P002": 1})
        orders = self.ecommerce.list_orders()
        self.assertEqual(len(orders), 3)
        self.assertIn("O003", orders[-1])

    def test_cancel_order(self):
        response = self.ecommerce.cancel_order("O001")
        self.assertIn("Order O001 has been canceled", response)
        self.assertEqual(len(self.ecommerce.orders), 1)

    def test_get_orders_in_date_range(self):
        customer = next(c for c in self.ecommerce.customers if c.customer_id == "C001")
        order_date = (datetime.date.today() - datetime.timedelta(days=10)).strftime("%Y-%m-%d")
        self.ecommerce.place_order("O003", "C001", {"P002": 1})
        self.ecommerce.orders[-1].order_date = datetime.datetime.strptime(order_date, "%Y-%m-%d").date()
        start_date = (datetime.date.today() - datetime.timedelta(days=15)).strftime("%Y-%m-%d")
        end_date = (datetime.date.today() - datetime.timedelta(days=5)).strftime("%Y-%m-%d")
        orders_in_range = self.ecommerce.get_orders_in_date_range(start_date, end_date)
        self.assertEqual(len(orders_in_range), 1)
        self.assertEqual(orders_in_range[0].order_id, "O003")

    def test_generate_customer_order_history(self):
        history = self.ecommerce.generate_customer_order_history("C001")
        self.assertIn("Order ID: O001", history)
        self.assertIn("Laptop", history)

    # === Report and Analytics Tests ===
    def test_generate_sales_report(self):
        report = self.ecommerce.generate_sales_report()
        self.assertIn("Total Sales: $2450", report)

    def test_find_most_purchased_product(self):
        most_purchased = self.ecommerce.find_most_purchased_product()
        self.assertIsNotNone(most_purchased)
        self.assertEqual(most_purchased.product_id, "P003")

    def test_generate_customer_spending_report(self):
        report = self.ecommerce.generate_customer_spending_report()
        self.assertIn("Alice: $2000.00", report)
        self.assertIn("Bob: $450.00", report)

    def test_find_top_selling_product(self):
        top_product = self.ecommerce.find_top_selling_product()
        self.assertIn("Top Selling Product: Table (Sold: 3 units)", top_product)

    def test_customer_purchase_history(self):
        history = self.ecommerce.customer_purchase_history("C001")
        self.assertIn("Purchase History for Alice:", history)
        self.assertIn("Laptop", history)
        self.assertIn("Phone", history)

        self.ecommerce.add_customer("C003", "Charlie", "charlie@example.com", "5555555555")
        history = self.ecommerce.customer_purchase_history("C003")
        self.assertEqual(history, "No purchases found.")

        history = self.ecommerce.customer_purchase_history("C999")
        self.assertEqual(history, "Customer not found.")

    def test_update_customer_email(self):
        # Case 1: Valid email update
        response = self.ecommerce.update_customer_email("C001", "alice_new@example.com")
        customer = next(c for c in self.ecommerce.customers if c.customer_id == "C001")
        self.assertEqual(customer.email, "alice_new@example.com")
        self.assertIn("Email for Alice updated to alice_new@example.com", response)

        # Case 2: Non-existent customer ID
        with self.assertRaises(ValueError) as context:
            self.ecommerce.update_customer_email("C999", "invalid@example.com")
        self.assertEqual(str(context.exception), "Customer not found.")

    def test_get_highest_spending_customer(self):
        highest_spender = self.ecommerce.get_highest_spending_customer()
        self.assertIsNotNone(highest_spender)
        self.assertEqual(highest_spender.customer_id, "C001")  # Based on setup, Alice spends more

        self.ecommerce.customers.clear()  # Remove all customers
        response = self.ecommerce.get_highest_spending_customer()
        self.assertEqual(response, "No customers available.")


    def test_find_customers_with_high_spending(self):
        high_spenders = self.ecommerce.find_customers_with_high_spending(1000)
        self.assertEqual(len(high_spenders), 1)
        self.assertEqual(high_spenders[0].customer_id, "C001")

        high_spenders = self.ecommerce.find_customers_with_high_spending(5000)
        self.assertEqual(len(high_spenders), 0)

        self.ecommerce.add_customer("C003", "Charlie", "charlie@example.com", "5555555555")
        high_spenders = self.ecommerce.find_customers_with_high_spending(0)
        self.assertEqual(len(high_spenders), 2)  # Charlie has not made purchases yet

    def test_find_orders_by_date(self):
        target_date = datetime.date.today().strftime("%Y-%m-%d")
        orders = self.ecommerce.find_orders_by_date(target_date)
        self.assertEqual(len(orders), 2)  # Two orders placed during setup

        future_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        orders = self.ecommerce.find_orders_by_date(future_date)
        self.assertEqual(len(orders), 0)

        with self.assertRaises(ValueError):
            self.ecommerce.find_orders_by_date("invalid-date")


if __name__ == "__main__":
    unittest.main()
