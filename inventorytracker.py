# Inventory Tracker Program
# Author: Jose Dones
# This program helps track products that are bought for resale.
# It allows the user to:
# 1. Add a new product
# 2. Record when a product has been sold
# 3. View a list of products that are still pending sale
# The program saves product data in CSV files so the information remains stored
# even after the program is closed.
import os
from datetime import datetime as datetime
import csv

# This function displays the main menu and asks the user to choose
# an option from 1 to 4. It keeps asking until the user enters
# a valid menu choice.
def menu():
    print( """
          MAIN MENU:
        1.ADD PRODUCT
        2.ADD A SELL
        3.LIST OF PRODUCTS
        4.EXIT PROGRAM
""")
    while True:
        choice = input("Please type a number from 1 to 4: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= 4:
            return int(choice)
        print("Please type a valid number option from 1 to 4: ")

    # This function asks the user for a number, such as a cost, shipping amount,
# or sale price. It removes invalid characters and keeps asking until
# the user enters a valid dollar amount.
def get_number(prompt):
    while True:
        p = input(prompt).strip()
        cleaned = ''.join(ch for ch in p if ch.isdigit() or ch in '.-')
        if cleaned in ("","-",".",".-"):
            print("Please type in a valid dollar amount. Example 12, 12.50,, 12.0. ")
            continue
        try:
            return float(cleaned)
        except ValueError:
            print("Invalid, please try again. ")

# This function creates the next product ID.
# If the products file does not exist yet, it starts with P0001.
# Otherwise, it counts the number of products already saved
# and creates the next ID in sequence.
def next_product_id():
    if not os.path.exists("products.csv"):
        return ("P0001")
    with open("products.csv", "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        count = sum(1 for _ in reader)
    return f'P{count+1:04d}'

    # This function saves a newly added product into products.csv.
# If the file does not already contain data, it first writes the header row.
def save_new_product(product_id, date, product, cost, shipping, total):
    exists = os.path.exists('products.csv') and os.path.getsize('products.csv') > 0
    with open('products.csv', 'a', newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["product_id", "date", "product", "cost", "shipping", "total"])
        writer.writerow([
            product_id,
            date,
            product,
            f'{cost:.2f}',
            f'{shipping:.2f}',
            f'{total:.2f}'
        ])

# This function collects product information from the user,
# calculates the total cost, suggests a sale goal,
# saves the product to the CSV file,
# and then lets the user say whether the item has already been sold.
def add_product():
    product_id = next_product_id()
    product = input("What product do you want to add?: ")
    cost = get_number("How much did you pay for the product? ( do not include shipping): ")
    shipping = get_number("How much did you pay for shipping?: ")
    total = cost + shipping
    date = datetime.now().strftime("%Y,%m,%d")
    sell_for = total * 2
    print(f'The goal is to sell this product for ${sell_for} dollars.')

    save_new_product(product_id, date, product, cost, shipping, total)

    print(f"\n Product added {product} under {product_id}: {product}")
    print(f" Cost: ${cost:.2f}")
    print(f" Shipping: ${shipping:.2f}")
    print(f" Total: ${total:.2f}")

    ifsold = input("Did you already sell this product? (answer with yes or no): ").strip().lower()
    if ifsold == "no":
        print("Ok, product still needs to be sold.")
        return 
    else:
        print("Ok, go back to the main menu and select option 2 (ADD A SELL).")

# This function loads all products from products.csv.
# If the file does not exist or is empty, it returns an empty list.
# Each product is stored as a dictionary.
def load_product():
    if not os.path.exists('products.csv') or os.path.getsize('products.csv') == 0:
        return []
    with open('products.csv', 'r', newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader if row and row.get("product_id")]

def load_sold_id():
    if not os.path.exists('soldproducts.csv') or os.path.getsize('soldproducts.csv') == 0:
        return set()
    with open('soldproducts.csv', 'r', newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        ids = set()
        for row in reader:
            p_id = (row.get("product_id") or "").strip().lower()
            ids.add(p_id.strip().upper())
            if p_id:
                ids.add(p_id)
        return ids

# This function saves a sold product record into soldproducts.csv.
# It stores the product ID, the date sold, and the selling price.
def save_sold_product(product_id, date_sold, sold_for):
    product_id = product_id.strip().upper()
    exists = os.path.exists("soldproducts.csv")
    with open('soldproducts.csv', 'a', newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["product_id", "date_sold", "sold_for"])
        writer.writerow([product_id, date_sold, f"{sold_for:.2f}"])

# This function allows the user to record the sale of a product.
# It loads all products, removes the ones already sold,
# asks the user which product was sold,
# calculates profit or loss,
# saves the sold product data,
# and then confirms the sale was saved.
def add_sold_product():
    product = load_product()
    sold_ids = load_sold_id()
    available = [c for c in product if c["product_id"] not in sold_ids]
    if not available:
        print("There are no items available for sell.\n")
        return
    print("\m Products pending sell: ")
    for P in available:
        print(f'{P["product_id"]} - {P["product"]} (Total ${float(P["total"]):.2f})')
    product_id = input("\nPlease type the number ID of the product you sold. (Example: P0001): ").strip().upper()
    products = next((p for p in available if p["product_id"] == product_id), None)
    if not products:
        print("Invalid ID or product has already been sold.\n")
    total = float(products["total"])
    sell_for = total * 2
    sold_for = get_number("How much did you sell the product for?: ")
    profit = sold_for - total

    if sold_for > sell_for:
        extra = sold_for - sell_for
        print(f'Congrats, you have a profit of ${profit:.2f}. Which is ${extra:.2f} more than the goal.')
    elif sold_for < total:
        loss = total - sold_for
        print(f'You have a loss of -${loss:.2f} dollars.')
    elif sold_for == sell_for:
        print("Perfect, You sold the product for the expected amount.")
    else:
        missing = sell_for - sold_for
        print(f'You have a profit of ${profit:.2f} but you were missing ${missing:.2f} dollars to reach goal.')
    date_sold = datetime.now().strftime("%Y,%m,%d")
    sold_norm = {v.strip().upper() for v in sold_ids}
    pending = [p for p in product if p["product_id"].strip().upper() not in sold_norm]
    save_sold_product(product_id, date_sold, sold_for)
    print("Product sold saved.\n")

# This function lists all products and shows which ones are still pending sale.
# It loads all products, loads all sold product IDs,
# compares them, and prints the products that have not been sold yet.
def list_of_products():
    product = load_product()
    sold_ids = load_sold_id()
    sold_norm = {v.strip().upper() for v in load_sold_id()}

    pending = []
    for p in product:
        p_id = (p.get("product_id") or "").strip().upper()
        if p_id and p_id not in sold_norm:
            pending.append(p)
    print("\nLIST")
    print(f"Products: {len(product)} | Pending: {len(pending)}")

    print("\nPending products for sell: ")
    for p in pending:
        print(f'- {p["product_id"]}: {p["product"]} (total ${float(p["total"]):.2f})')

# This is the main control function for the program.
# It keeps showing the menu until the user chooses to exit.
def main():
    while True:
        choice = menu()
        if choice == 1:
            add_product()
        elif choice == 2:
            add_sold_product()
        elif choice == 3:
            list_of_products()
        else:
            print("Exiting program. ")
            quit()
# This starts the program only when the file is run directly.
if __name__ == "__main__":
    main()
