from datetime import datetime
import random

class Coffee:
    def __init__(self, name, base_price):
        self.name = name
        self.base_price = base_price

    def get_price_by_size(self, size):
        size = size.lower()
        if size == "small":
            return self.base_price
        elif size == "medium":
            return self.base_price + 0.5
        elif size == "large":
            return self.base_price + 1.0
        else:
            return self.base_price

class OrderedItem:
    def __init__(self, coffee_name, size, price, quantity):
        self.name = coffee_name
        self.size = size
        self.price = price
        self.quantity = quantity

class Order:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.customer_id = f"CUST{random.randint(1000, 9999)}"
        self.user = f"{first_name}_{last_name}"
        self.items = []

    def add_item(self, coffee):
        size = input("Choose size (S/M/L): ").strip().lower()
        if size not in ['s', 'm', 'l']:
            print("❌ Invalid size selected. Please try again.")
            return
        try:
            quantity = int(input("How many would you like?: "))
            if quantity <= 0:
                print("❌ Quantity must be at least 1.")
                return
        except ValueError:
            print("❌ Invalid quantity. Please enter a number.")
            return

        final_price = coffee.get_price_by_size(size)
        item = OrderedItem(coffee.name, size, final_price, quantity)
        self.items.append(item)
        print(f"✅ Added {quantity} {size.title()} {coffee.name}(s) to your order.")

    def total(self):
        return sum(item.price * item.quantity for item in self.items)

    def discount(self):
        total = self.total()
        return total * 0.10 if total >= 50 else 0

    def final_total(self):
        return self.total() - self.discount()

    def show_order(self):
        if not self.items:
            print("No items in order.")
            return

        print("\n🧾 Your Order:")
        print("=" * 60)
        print("{:<5} {:<15} {:<10} ${:<10} ${:<10}".format("Qty", "Item", "Size", "Price", "Total"))
        print("-" * 60)

        for item in self.items:
            line_total = item.price * item.quantity
            print("{:<5} {:<15} {:<10} ${:<9.2f} ${:<.2f}".format(
                item.quantity, item.name, item.size.title(), item.price, line_total
            ))

        print("-" * 60)
        print(f"{'Subtotal:':<45} ${self.total():.2f}")
        if self.discount() > 0:
            print(f"{'Discount (10%):':<45} -${self.discount():.2f}")
        print(f"{'Total to pay:':<45} ${self.final_total():.2f}")
        print("=" * 60)

    def checkout(self):
        if not self.items:
            print("Your cart is empty.")
            return

        self.show_order()
        confirm = input("Proceed to checkout? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Checkout cancelled.")
            return

        total_cost = self.final_total()
        while True:
            try:
                paid = float(input(f"Your total is ${total_cost:.2f}. Enter payment amount: $"))
                if paid < total_cost:
                    print(f"❌ Insufficient payment. You still owe ${total_cost - paid:.2f}")
                    retry = input("Do you want to try again? (yes/no): ").strip().lower()
                    if retry != 'yes':
                        print("❌ Payment cancelled.")
                        return
                else:
                    change = paid - total_cost
                    print(f"✅ Payment accepted. Your change is ${change:.2f}")
                    break
            except ValueError:
                print("❌ Invalid input. Please enter a number.")

        # Save individual receipt
        try:
            timestamp = datetime.now().strftime("%y-%m-%d_%H-%M-%S")
            filename = f"receipt_{self.user}_{timestamp}.txt".replace(" ", "_")
            with open(filename, "w", encoding="utf-8") as f:
                f.write("🧾 Coffee Order Receipt\n")
                f.write("=" * 40 + "\n")
                f.write(f"Customer ID: {self.customer_id}\n")
                f.write(f"Name: {self.first_name} {self.last_name}\n")
                if self.email:
                    f.write(f"Email: {self.email}\n")
                f.write(f"Time: {datetime.now()}\n")
                f.write("=" * 40 + "\n")
                f.write("{:<5} {:<12} {:<8} {:<7} {:<7}\n".format("Qty", "Item", "Size", "Price", "Total"))
                f.write("-" * 40 + "\n")
                for item in self.items:
                    line_total = item.quantity * item.price
                    f.write("{:<5} {:<12} {:<8} ${:<6.2f} ${:<.2f}\n".format(
                        item.quantity, item.name, item.size.title(), item.price, line_total
                    ))
                f.write("-" * 40 + "\n")
                f.write(f"{'Subtotal:':<30} ${self.total():.2f}\n")
                if self.discount() > 0:
                    f.write(f"{'Discount (10%):':<30} -${self.discount():.2f}\n")
                f.write(f"{'Total:':<30} ${self.final_total():.2f}\n")
                f.write(f"{'Paid:':<30} ${paid:.2f}\n")
                f.write(f"{'Change:':<30} ${change:.2f}\n")
                f.write("=" * 40 + "\n")
                f.write("Thank you for your order!\n")
        except Exception as e:
            print(f"Failed to save receipt: {e}")

        # Append to orders log
        try:
            with open("Orders.txt", "a", encoding="utf-8") as f:
                f.write(f"Customer: {self.first_name} {self.last_name}\n")
                for item in self.items:
                    f.write(f"{item.quantity} x {item.size.title()} {item.name} @ ${item.price:.2f} each\n")
                f.write(f"Total: ${self.total():.2f}\n")
                f.write("-" * 30 + "\n")
        except Exception as e:
            print(f"Failed to save Orders.txt: {e}")

        self.items.clear()

def main():
    first = input("Enter your first name: ").strip()
    last = input("Enter your last name: ").strip()
    email = input("Enter your email (optional): ").strip()

    print(f"\nWelcome, {first}!\n")
    order = Order(first, last, email)

    menu = [
        Coffee("Espresso", 2.5),
        Coffee("Latte", 3.5),
        Coffee("Cappuccino", 3.0),
        Coffee("Americano", 2.0)
    ]

    while True:
        print("\n--- Coffee Menu ---")
        for i, coffee in enumerate(menu, 1):
            print(f"{i}. {coffee.name} - Base price: ${coffee.base_price}")
        print("5. View Order")
        print("6. Checkout")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice in ['1', '2', '3', '4']:
            order.add_item(menu[int(choice) - 1])
        elif choice == '5':
            order.show_order()
        elif choice == '6':
            order.checkout()
        elif choice == '7':
            print("Thanks for visiting. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()




