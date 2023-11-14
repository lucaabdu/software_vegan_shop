import json
# Let's try and load the files, if they exist
## otherwise, generate two empty dictionnaries
try:
    with open('inventory.json', 'r') as json_inv, open('sales_sheet.json', 'r') as json_sales:
            inventory = json.load(json_inv)
            sales_sheet = json.load(json_sales)
except (json.JSONDecodeError, FileNotFoundError): # Handle the case where the file is empty or not valid JSON
    inventory = {}
    sales_sheet = {}
    
# Main body of the script
while True: # infinite loop to go back to the command input
    accepted_commands = ['add', 'list', 'sell', 'profits', 'help', 'close']
    
    # functions
    def add_new_product():
        """
        This function adds a new product to the inventory or updates its quantity if the product is already 
        present in the inventory
        """
        new_product = str(input('Name of the product, "exit" to go back '))
        if new_product == 'exit':
            return
        while True:
            try:
                quantity = float(input('Quantity, "0" to exit: '))
                if quantity == 0:
                    return
                assert(quantity >= 0), 'Quantity must be positive'
                break
            except ValueError:
                print('Quantity must be a number')
            except AssertionError as e:
                print(e)
        if new_product in inventory: 
            inventory[new_product][0] = inventory[new_product][0] + quantity
            # I preferred using a list instead of a nested dictionnary
        else:
            inventory[new_product] = [] # I preferred using a list instead of a nested dictionnary
            while True:
                try:
                    purch_price = float(input('Purchase price, "0" to exit: '))
                    if purch_price == 0:
                        return
                    assert(purch_price >= 0), 'Purchase price must be a positive number'
                    break
                except ValueError:
                    print('Purchase price must be a number')
                except AssertionError as e:
                    print(e)
            while True:
                try:
                    sell_price = float(input('Selling price, "0" to exit: '))
                    if sell_price == 0:
                        return
                    assert(sell_price >= 0), 'Selling price must be a positive number'
                    break
                except ValueError:
                    print('Selling price must be a number')
                except AssertionError as e:
                    print(e)
                
            inventory[new_product] = [quantity, purch_price, sell_price]
        print(f'ADDED: {quantity} X {new_product}')
        return
    def list_products():
        """
        This function returns the list of all the products in the inventory with their quantities and 
        selling prices
        """
        col_names = ('PRODUCT', 'QUANTITY', 'PRICE')
        print(f'{col_names[0]:<15} {col_names[1]:<10} {col_names[2]}')

        for i in inventory:
            print(f'{i:<15} {inventory[i][0]:<10.2f} €{inventory[i][2]:.2f}')
    def sell_a_product():
        """
        This function adds a new sale to the sales sheet and reduces the quantity in the inventory
        """
        while True:
            try:
                sell_a_product.sold_product = str(input('Name of the product, "0" to exit: '))
                if sell_a_product.sold_product == 'exit':
                    return
                assert(sell_a_product.sold_product in inventory),\
                'The product is not in stock'
                assert(inventory[sell_a_product.sold_product][0] != 0),\
                'The product is out of stock'
                break
            except AssertionError as e:
                print(e)
        while True:
            try:
                quantity = float(input('Quantity, "0" to exit: '))
                if quantity == 0:
                    return
                assert(quantity <= inventory[sell_a_product.sold_product][0]),\
                'The quantity in stock is not sufficient'
                assert(quantity >= 0), 'Quantity must be positive'
                break
            except ValueError:
                print('Quantity must be a number')
            except AssertionError as e:
                print(e)
        
        inventory[sell_a_product.sold_product][0] =  inventory[sell_a_product.sold_product][0]\
        - quantity          
        if sell_a_product.sold_product in sales_sheet:
            sales_sheet[sell_a_product.sold_product][0] += quantity
        else:
            sales_sheet[sell_a_product.sold_product] = [quantity, inventory[sell_a_product.sold_product][2]]
        return
    def register_sales():
        """
        This function registers a sale and it gives the possibility to add an additional sale if needed.
        It returns a little recap of the sales registered.
        """
        sell_a_product()
        if sell_a_product.sold_product == 'esci':
            return
        added_products = [sell_a_product.sold_product]
        while True:
            add_sale = str(input('Add a new product: (yes/no): '))
            if add_sale == 'yes':
                sell_a_product()
                added_products.append(sell_a_product.sold_product)
            elif add_sale == 'no':
                total = 0
                print('SALE REGISTERED:')
                for prod in added_products:
                    print(f'- {sales_sheet[prod][0]} X {prod}: €{sales_sheet[prod][1]:.2f}')
                    total += sales_sheet[prod][0]*sales_sheet[prod][1]
                print(f'Totale: €{total:.2f}')
                break
    
    def profits():
        """
        This function returns the gross and net profits of the shop
        """
        gross_profit = 0
        cogs = 0 #cost of goods sold
        for sale in sales_sheet:
            gross_profit += sales_sheet[sale][0] * sales_sheet[sale][1] 
            # index memento: 0 is the quantity, 1 is the selling price in sales sheet
            cogs += sales_sheet[sale][0] * inventory[sale][1]
            # index memento: 0 is the quantity, 1 is the purchase price in the inventory
        net_profit = gross_profit - cogs
        print(f'Gross profits: €{gross_profit:.2f}')
        print(f'Net profits: €{net_profit:.2f}')
                          
    def exec_command(command):
        """
        This function executes the command given in input
        """
        if command == 'add':
            add_new_product()
        elif command == 'sell':
            register_sales()
        elif command == 'help':
            print('The ' + str_command_error[26:])
        elif command == 'list':
            list_products()
        elif command == 'profits':
            profits()
        elif command == 'close':
            print('Bye Bye')
            return True  # Return True to indicate that the loop should be broken 
    
    # Start of the program
    command = input('Insert a command, "close" to exit; "help" to get help: ')
    
    str_command_error = str('The command is not valid, valid commands are the following: \n'+
                     '- add: add a product to the inventory \n'+
                     '- list: list all the products in the inventory \n'+
                     '- sell: register new sales \n'+
                     '- profits: show gross and net profits \n'+
                     '- help: list all the possible commands \n'+
                     '- clost: exit the program')
    if not command in accepted_commands:
        print(str_command_error)
    if exec_command(command):
        break  # Break the loop if exec_command returns True

# Saving the data in JSON files for future use
with open('inventory.json', 'w') as json_inv, open('sales_sheet.json', 'w') as json_sales:
    json.dump(inventory, json_inv, indent = 6)
    json.dump(sales_sheet, json_sales, indent = 6)