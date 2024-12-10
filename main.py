from ecommerce.ecommerce import ECommerce

def main():
    print("Welcome to the E-Commerce Management System!")
    ecommerce = ECommerce()

    while True:
        print("\nMenu:")
        print("1. Add Product")
        print("2. List Products")
        print("3. Add Customer")
        print("4. List Customers")
        print("5. Place Order")
        print("6. List Orders")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            product_id = input("Enter product ID: ")
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            stock = int(input("Enter product stock: "))
            category = input("Enter product category: ")
            ecommerce.add_product(product_id, name, price, stock, category)
            print(f"Product '{name}' added successfully.")

        elif choice == "2":
            print("\nProducts:")
            products = ecommerce.list_products()
            if products:
                for product in products:
                    print(product)
            else:
                print("No products available.")

        elif choice == "3":
            customer_id = input("Enter customer ID: ")
            name = input("Enter customer name: ")
            email = input("Enter customer email: ")
            phone_number = input("Enter customer phone number: ")
            ecommerce.add_customer(customer_id, name, email, phone_number)
            print(f"Customer '{name}' added successfully.")

        elif choice == "4":
            print("\nCustomers:")
            customers = ecommerce.list_customers()
            if customers:
                for customer in customers:
                    print(customer)
            else:
                print("No customers available.")

        elif choice == "5":
            order_id = input("Enter order ID: ")
            customer_id = input("Enter customer ID: ")
            print("Enter product IDs and quantities (type 'done' to finish):")
            items = {}
            while True:
                product_id = input("Product ID: ")
                if product_id.lower() == "done":
                    break
                quantity = int(input("Quantity: "))
                items[product_id] = quantity
            try:
                ecommerce.place_order(order_id, customer_id, items)
                print("Order placed successfully.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "6":
            print("\nOrders:")
            orders = ecommerce.list_orders()
            if orders:
                for order in orders:
                    print(order)
            else:
                print("No orders available.")

        elif choice == "7":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
