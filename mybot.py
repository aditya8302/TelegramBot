import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define your bot's token
TOKEN = "5687695797:AAFV8Vz9QmR3WbfTudrA0rJxhN-rT6K2x9E"
# bot name = @adityalocalgenralstorebot

inventory_list=[
    {
        'Name':'Atta',
        'Brand':'Ashirwaad',
        'Weight': '1kg',
        'Price':65,
        'remaining-quantity':12,
    },
    {
        'Name':'Rice',
        'Brand':'India Gate',
        'Weight': '1kg',
        'Price':80,
        'remaining-quantity':60,
    },
    {
        'Name':'Maida_Flour',
        'Brand':'Sharbati',
        'Weight': '500g',
        'Price':89,
        'remaining-quantity':32,
    },
    {
       'Name':'Besan',
        'Brand':'Fortune',
        'Weight': '500g',
        'Price':65,
        'remaining-quantity':47,
    },
    {'Name':'Yellow_Moong_Dal',
        'Brand':'Tata Sampann Organic',
        'Weight': '500g',
        'Price':136,
        'remaining-quantity':15,
    },    
    {'Name':'Chana_Dal',
        'Brand':'Tata Sampann Organic',
        'Weight': '500g',
        'Price':92,
        'remaining-quantity':11,
    },
    {'Name':'Red_Chilli_Powder',
        'Brand':'Catch Red Chilli',
        'Weight': '500g',
        'Price':255,
        'remaining-quantity':7,
    },
    {'Name':'Chana_Dal',
        'Brand':'Tata_Sampann_Organic',
        'Weight': '500g',
        'Price':92,
        'remaining-quantity':11,
    },
    {'Name':'Powder_Salt',
        'Brand':'Tata Salt Iodized',
        'Weight': '1Kg',
        'Price':24,
        'remaining-quantity':17,
    },
    {'Name':'Cooking_Oil',
        'Brand':'Fortune Soyabean Oil',
        'Weight': '1L',
        'Price':150,
        'remaining-quantity':8,
    },
    {'Name':'Noodles_and_Pasta',
        'Brand':'Nestle Maggi',
        'Weight': '4',
        'Price':80,
        'remaining-quantity':10,
    },
    {'Name':'Tea_Powder',
        'Brand':'Taj Mahal',
        'Weight': '100g',
        'Price':45,
        'remaining-quantity':20,
    },
    {'Name':'Toothpaste',
        'Brand':'Colgate',
        'Weight': '100g',
        'Price':59,
        'remaining-quantity':19,
    },
    {'Name':'Shampoo',
        'Brand':'Himalaya',
        'Weight': '100ml',
        'Price':120,
        'remaining-quantity':8,
    },
]

current_order=[]
# Define the start command handler
def start(update: Update, context):
    """Send a welcome message when the command /start is issued."""
    update.message.reply_text('Welcome to your local general store inventory Telegram bot! Type /help to see available commands.')

# Define the help command handler
def help(update: Update, context):
    """Send a help message when the command /help is issued."""
    update.message.reply_text('Available commands:\n'
                              '/start - Start the bot\n'
                              '/help - Show available commands\n'
                              '/add_item - Add an item to the inventory\n'
                              '/remove_item - Remove an item from the inventory\n'
                              '/order - Order Items\n'
                              '/view_inventory - View the current inventory'
                              '/feedback - to give feedback to us')

# Define the add_item command handler
def add_item(update: Update, context):
    """Add an item to the inventory."""

    message=update.message.text.split(' ')
    message.pop(0)
    price=0
    for i in inventory_list:
        if i['Name'].lower()==message[0].lower():
            price=i['Price']*int(message[1])
    item={
        'name':message[0],
        'quantity':message[1],
        'Price':price
    }
    current_order.append(item)
    update.message.reply_text(f'{message[0]} Successfully added to the list')


# Define the remove_item command handler
def remove_item(update: Update, context):
    """Remove an item from the inventory."""
    message=update.message.text.split(' ')
    message.pop(0)
    for i in current_order:
        if i['name'].lower()==message[0].lower():
            current_order.remove(i)

    update.message.reply_text(f'{message[0]} Successfully removed to the list')

# Define the view_inventory command handler
def view_inventory(update: Update, context):
    """View the current inventory."""
    # Get the current inventory (replace this with your own implementation)
    # Add your code here
    # Format the inventory information
    inventory_info = 'Inventory choose item'

    for i in inventory_list:
        inventory_info=inventory_info+'\n /'+i['Name']

    update.message.reply_text(inventory_info)

def order(update: Update,context):

    reply="Current cart list\n"
    total=0

    for i in current_order:
        reply=reply+i['name']+" "+i["quantity"]+"units "+str(i["Price"])+'Rs\n'
        total+=i["Price"]

    reply=reply+"\nTotal Cost= "+str(total)
    reply=reply+'\n Enter /add_item item_name quantity : to add it in the list\n'
    reply=reply+'\n Enter /remove_item item_name : to remove item from order list /final_order : order the above listed orders'
    update.message.reply_text(reply)
    

# Define the echo message handler
def echo(update: Update, context):
    """Echo the received message."""
    update.message.reply_text(update.message.text)

def create_function(n,st):
    func_string = f"def power_{n}(update: Update, context):\n    update.message.reply_text(f'{st}')"
    exec(func_string)
    return locals()[f"power_{n}"]

def final_order(update:Update,context):
    for i in current_order:
        current_order.remove(i)
    update.message.reply_text("Succefully ordered the current list")

def feedback(update, context):
    user = update.message.from_user
    message = update.message.text
    # Save the feedback to a database or file
    # Or send the feedback to an email address or Slack channel
    reply_text = 'Thank you for your feedback!'
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)

def main():
    """Start the bot."""    
    # Create an instance of the Updater class with your bot's token
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('add_item', add_item))
    dp.add_handler(CommandHandler('remove_item', remove_item))
    dp.add_handler(CommandHandler('view_inventory',view_inventory))
    dp.add_handler(CommandHandler('order',order))
    dp.add_handler(CommandHandler('final_order',final_order))
    dp.add_handler(CommandHandler('feedback',feedback))

    for i in inventory_list:
        temp=""
        for key,value in i.items():
            if(isinstance(value, int)):
                temp= temp+key+': '+str(value)+'\t'
            else:
                temp=temp+key+': '+value+'\t'

        item_funct=create_function(i['Name'],temp)
        dp.add_handler(CommandHandler(i['Name'],item_funct))
    updater.start_polling()
main()
