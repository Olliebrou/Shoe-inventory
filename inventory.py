from tabulate import tabulate


# ========The beginning of the class==========
class Shoe:
    """
    Shoe class for each shoe product. It contains a constructor taking the shoe's
    country, product code, name, cost, and stock quantity.
    """
    def __init__(self, country, code, product, cost, quantity):
        """
        Constructor for Shoe class taking:
        country, code, product name, cost and stock quantity
        """
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        """
        Method for Shoe class
        :return: Shoe object's cost in Rands
        """
        return self.cost

    def get_quantity(self):
        """
        Method in Shoe class
        :return: Quantity of shoes in stock
        """
        return self.quantity

    def get_value(self):
        """
        Method in Shoe class
        :return: Value of shoe product in stock
        """
        return self.cost * self.quantity

    def __str__(self):
        """
        String method in Shoe class
        :return: String representation of shoe object
        """
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"


# Dictionary containing shoe's code as key for each shoe object
shoe_code_dict = {}


def read_shoes_data():
    """
    Reads all the data from inventory.txt file
    adds each line as a shoe object to shoe dictionary.
    """
    try:
        with open('inventory.txt', 'r') as f:
            next(f)                                     # Skips the first descriptor line
            for line in f:
                line = line.split(",")                  # Splits each line into its data
                this_shoe = Shoe(line[0], line[1], line[2], int(line[3]), int(line[4]))
                shoe_code_dict[line[1]] = this_shoe     # Key = code  Value = shoe object
    except FileNotFoundError:
        print("Inventory file not found")
    except ValueError or IndexError:
        print("Incorrect format in inventory file")


def capture_shoes():
    """
    Asks user to input data for new shoe object and adds it to shoe dictionary
    """
    print("Please enter the following shoe data:")
    country = input("Country: ")
    code = input("Code: ")
    product = input("Product name: ")
    cost = input("Cost in Rands: ")
    quantity = input("Quantity: ")
    try:
        shoe_code_dict[code] = Shoe(country, code, product, int(cost), int(quantity))
        print("\nShoe added successfully")
    except ValueError:
        print("Oops! You have entered the cost or quantity incorrectly."
              "Please try again only entering the number value\n")
    update_inventory()                          # Adds new shoe to inventory.txt


def view_all():
    """
    Sends all shoe objects to be printed out by display_shoes function.
    """
    display_shoes(shoe_code_dict.values())


def display_shoes(shoe_object_list):
    """
    Takes in a list of shoe objects and displays them in a table using tabulate function
    """
    table = [i.__str__().split(",") for i in shoe_object_list]
    print(tabulate(table, headers=["Country", "Code", "Product", "Cost (R)", "Quantity"]))


def re_stock():
    """
    Finds the shoe object with the lowest stock quantity,
    Asks the user to input the amount to restock by,
    Then changes the shoe quantity to new quantity
    """
    shoe = min(shoe_code_dict.values(), key=lambda x: x.get_quantity())
    print(f"The shoe that needs to be restocked is {shoe.product} with {shoe.get_quantity()} in stock.")
    restock = input("Please enter the number of new shoes to restock:   ")
    try:
        shoe_code_dict[shoe.code].quantity += int(restock)
        print(f"{shoe.product} has been restocked and now has {shoe_code_dict[shoe.code].quantity} in stock.")
    except ValueError:
        print("Oops! That is not a valid number. Please try again")
    update_inventory()


def update_inventory():
    """
    Writes the current shoe objects from dictionary to inventory.txt file as string notations.
    """
    with open('inventory.txt', 'w') as f:
        f.write("Country,Code,Product,Cost,Quantity\n")
        for shoe in shoe_code_dict.values():
            f.write(shoe.__str__() + "\n")


def search_shoe():
    """
    Finds a shoe by user entered code and displays corresponding shoe.
    """
    code = str(input("Please enter the shoe code e.g SKU00000"))
    if code in shoe_code_dict:
        shoe_in_list = [shoe_code_dict[code]]
        display_shoes(shoe_in_list)
    else:
        print("Shoe not found. Please try again")


def value_per_item():
    """
    Prints a table of the codes, names, and stock value of all shoes stored.
    """
    table = []
    for i in shoe_code_dict.values():
        table.append([i.code, i.product, i.get_value()])
    print(tabulate(table, headers=["Shoe code", "Shoe name", "Stock value (R)"]))


def highest_qty():
    """
    Finds the shoe with the highest stock quantity,
    asks the user to enter the amount to mark the price of the shoe down by,
    then overwrites the shoe's cost to the new value.
    """
    shoe = max(shoe_code_dict.values(), key=lambda x: x.get_quantity())
    print(f"""The shoe to mark down for sale is {shoe.product} at R{shoe.cost} each.
There are currently {shoe.get_quantity()} in stock in {shoe.country}""")
    choice = input(f"""\nPlease enter the percent the {shoe.product} will be marked down by:
\nNormal price: R{shoe.get_cost()}
\n10% off = R{int(shoe.get_cost() * 0.9)}
20% off = R{int(shoe.get_cost() * 0.8)}
30% off = R{int(shoe.get_cost() * 0.7)}
40% off = R{int(shoe.get_cost() * 0.6)}
50% off = R{int(shoe.get_cost() * 0.5)}
\nPercent: """)
    try:
        shoe.cost = int(shoe.cost * ((100 - int(choice)) / 100))
    except ValueError:
        print("Only enter the number i.e 20")
    finally:
        shoe_code_dict[shoe.code] = shoe
    print(f"{shoe.product} marked for sale at R{shoe.cost}")
    update_inventory()


def delete_shoe():
    """
    Asks the user to enter the code for a shoe to be deleted
    then removes it from the dictionary and inventory.
    """
    code = str(input("Please enter the code for the shoe you wish to delete e.g SKU00000"))
    try:
        shoe_code_dict.pop(code)
        update_inventory()
        print("Shoe Deleted")
    except KeyError:
        print("That code does not exist! Please try again with a valid code.")


# ==========Main Menu=============
while True:
    read_shoes_data()
    print("\n==========Main Menu=============\nPlease enter one of the following:\n")
    menu_choice = input("""view - View inventory
add - Add new shoe product to inventory
search - Search shoe by product code
restock - Find shoes low in stock and restock
value - View all stock value
sale - Find shoe to mark for sale
delete - Delete a shoe from inventory
exit - Exit program\n""").lower()
    if menu_choice == "view":
        view_all()
    elif menu_choice == "add":
        capture_shoes()
    elif menu_choice == "search":
        search_shoe()
    elif menu_choice == "restock":
        re_stock()
    elif menu_choice == "value":
        value_per_item()
    elif menu_choice == "sale":
        highest_qty()
    elif menu_choice == "delete":
        delete_shoe()
    elif menu_choice == "exit":
        exit()
    else:
        print("Oops, you didn't make a correct choice, please try again.")
