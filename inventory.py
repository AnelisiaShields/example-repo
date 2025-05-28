"""This module provides regular expression matching"""
import re


# ========The beginning of the class==========
class Shoe:
    """Class that stores all the data for the shoe"""
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = float(cost)
        self.quantity = int(quantity)

    def get_cost(self):
        """returns the cost of the shoe in this method."""
        return self.cost

    def get_quantity(self):
        """Returns the quantity of the shoes."""
        return self.quantity

    def __str__(self):
        return (
            f"Product: {self.product}\n"
            f"Code: {self.code}\n"
            f"Country: {self.country}\n"
            f"Cost: {self.cost}\n"
            f"Quantity: {self.quantity}\n"
        )


# =============Shoe list===========
shoe_list = []


# ==========Functions outside the class==============
def read_shoes_data():
    """
    Reads shoe data from 'inventory.txt', creates Shoe objects, and
    adds them to the shoe_list.
    Parameters:
    None

    Returns:
    None
    """
    try:
        with open("inventory.txt", "r", encoding="utf-8") as file:
            next(file)  # Skips the header line
            for line in file:
                parts = line.strip().split(",")
                country = parts[0]
                code = parts[1]
                product = parts[2]
                cost = float(parts[3])
                quantity = int(parts[4])
                shoe_list.append(Shoe(country, code, product, cost, quantity))
    except FileNotFoundError:
        print("The file 'inventory.txt' was not found.")


def capture_shoes():
    """
    Captures user input for a new shoe, creates a Shoe object, and
    appends it to the shoe_list. Also writes the new shoe to inventory.txt.

    Parameters:
    None

    Returns:
    None
    """
    while True:
        country = input("Provide the product country: ").strip()
        if not country.replace(" ", "").isalpha():
            print("Invalid input. Please enter alphabetic characters only.")
        else:
            break

    while True:
        code = input(("Provide the product code (e.g. SKU123): ").strip()
                     .upper())
        if not re.fullmatch(r"SKU\d{5}", code):
            print("Invalid format. Code must be 'SKU' followed by five digits"
                  "(e.g. SKU123).")
        else:
            break

    while True:
        product = input("Provide the product name: ").strip()
        if not product.replace(" ", "").isalpha():
            print("Invalid input. Please enter alphabetic characters only.")
        else:
            break

    while True:
        try:
            cost = float(input("Provide the product cost: ").strip())
            if cost < 0:
                print("Cost cannot be negative. Please try again.")
            else:
                break
        except ValueError:
            print("Invalid cost. Please enter a valid number.")

    while True:
        try:
            quantity = int(input("Provide the product quantity: ").strip())
            if quantity < 0:
                print("Quantity cannot be negative. Please try again.")
            else:
                break
        except ValueError:
            print("Invalid quantity. Please enter an integer.")

    with open("inventory.txt", "a", encoding="utf-8") as file:
        file.write(f"{country},{code},{product},{cost},{quantity}\n")

    shoe_list.append(Shoe(country, code, product, cost, quantity))
    print("The shoe has been captured.")


def view_all():
    """
    Displays the details of all Shoe objects currently in the shoe_list
    in a table format using the tabulate module.

    Parameters:
    None

    Returns:
    None
    """
    if not shoe_list:
        print("No shoes in inventory.")
        return

    print(f"{'Country':<15} {'Code':<10} {'Product':<20} {'Cost':<10}"
          f"{'Quantity':<10}")
    print("-" * 65)
    for shoe in shoe_list:
        print(f"{shoe.country:<15} {shoe.code:<10} {shoe.product:<20}"
              f"{shoe.cost:<10.2f} {shoe.quantity:<10}")


def re_stock():
    """
    Identifies the Shoe object with the lowest quantity in shoe_list.
    Prompts the user to optionally add more stock and updates
    the inventory file.
    Parameters:
    None

    Returns:
    None
    """
    if not shoe_list:
        print("No shoe's available in inventory.")
        return
    lowest_shoe = min(shoe_list, key=lambda s: s.get_quantity())
    print(f"\nLowest stock item:\n{lowest_shoe}\n")
    choice = input("Do you want to restock this item? Type 'Yes' or"
                   " 'No': ").strip().lower()
    if choice == "yes":
        try:
            add_quantity = int(input("Enter the quantity to add: "))
            lowest_shoe.quantity += add_quantity
            print(f"Updated quantity: {lowest_shoe.quantity}")

            with open("inventory.txt", "w", encoding="utf-8") as file:
                file.write("Country,Code,Product,Cost,Quantity\n")
                for shoe in shoe_list:
                    file.write(f"{shoe.country},{shoe.code},{shoe.product},"
                               f"{shoe.cost},{shoe.quantity}\n")
            print("Inventory file updated successfully.")

        except ValueError:
            print("Invalid quantity entered.")
    else:
        print("No changes made to stock.")


def search_shoe():
    """
    Searches for a shoe in the shoe_list by its code and prints its
    details if found.
    Parameters:
    None

    Returns:
    None
    """
    search_code = input("Enter the shoe code you're searching for: ").strip()
    for shoe in shoe_list:
        if shoe.code.lower() == search_code.lower():
            print(shoe)
            return
    print("Shoe not found.")


def value_per_item():
    """
    Calculates and prints the total value (cost * quantity)
    for each shoe in the shoe_list.
    Parameters:
    None

    Returns:
    None
    """
    for shoe in shoe_list:
        value = shoe.cost * shoe.quantity
        print(f"{shoe.product} (Code: {shoe.code}) - Total Value: {value}")


def highest_qty():
    """
    Identifies and displays the shoe with the highest quantity,
    indicating it is on sale.
    Parameters:
    None

    Returns:
    None
    """
    if not shoe_list:
        print("No inventory loaded.")
        return
    most_stocked = max(shoe_list, key=lambda s: s.quantity)
    print(f"*** {most_stocked.product} is now on SALE! ***")
    print(most_stocked)


# ==========Main Menu============
def main():
    """
    Displays a menu for the user to interact with the shoe inventory system.
    Calls different functions based on user's choice.
    Parameter: 
    None

    Returns:
    None
    """
    read_shoes_data()

    while True:
        print("\n========= SHOE INVENTORY MENU =========")
        print("1 - View all shoes")
        print("2 - Capture new shoe")
        print("3 - Re-stock lowest quantity shoe")
        print("4 - Search for a shoe by code")
        print("5 - Display value per item")
        print("6 - Display product with highest quantity (on sale)")
        print("7 - Exit")

        choice = input("Enter your choice (1–7): ").strip()

        if choice == "1":
            view_all()
        elif choice == "2":
            capture_shoes()
        elif choice == "3":
            re_stock()
        elif choice == "4":
            search_shoe()
        elif choice == "5":
            value_per_item()
        elif choice == "6":
            highest_qty()
        elif choice == "7":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


# Call the main function to start the program
if __name__ == "__main__":
    main()

# I used google to figure out how to validate the user imputting an actual SKU:
# Link: https://www.tutorialspoint.com/python/python_re_fullmatch_method.htm#:~:text=The%20Python%20re.,of%20the%20string%20whereas%20re.

# I used google to figure out how to display my shoes in table format:
# Link : https://docs.python.org/3/library/string.html#format-specification-mini-language and
# https://stackoverflow.com/questions/27196501/format-strings-to-make-table-in-python-3

# I used google for calling the main function:
# Link : https://realpython.com/python-main-function/
