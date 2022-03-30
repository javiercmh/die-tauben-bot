"""
Simple Telegram bot to manage a shopping list.

List of commands:
/list - Show products in the shopping list
/add - Add product to the shopping list
/remove - Remove a product from the shopping list
/clear - Remove all products from the shopping list
/undo - Undo last action

Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import re
import pickle
import signal
import os
from xml.dom.minidom import Attr

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

updater = None
logger = logging.getLogger(__name__)
SHOPPING_LIST = list()
LIST_BACKUP = SHOPPING_LIST


def get_token() -> str:
    """Get the bot token from file."""
    with open('api.key') as f:
        return f.read().strip()


def restore_from_backup() -> None:
    """Retrieve shopping list from backup or start with an empty list."""
    global SHOPPING_LIST

    logger.info('Attempting to restore shopping list from backup...')
    
    try:
        with open('shopping_list.pkl', 'rb') as backup:
            SHOPPING_LIST = pickle.load(backup)
    except FileNotFoundError:
        pass

def shutdown(sig, frame):
    """Backup shopping list before shutdown."""
    global SHOPPING_LIST
    global updater

    logger.info('Backing up shopping list before shutdown')

    with open('shopping_list.pkl', 'wb') as backup:
        pickle.dump(SHOPPING_LIST, backup)
    
    updater.stop()


### Command handlers

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(f'Hi {user.mention_markdown_v2()}\!')
    update.message.reply_text('''List of commands:
/list - Show products in the shopping list
/add - Add product to the shopping list
/remove - Remove a product from the shopping list
/clear - Remove all products from the shopping list
/undo - Undo last action''')


def show_list(update: Update, context: CallbackContext) -> None:
    """Display shopping list when /list is issued."""
    global SHOPPING_LIST
    
    if len(SHOPPING_LIST) == 0:
        update.message.reply_text('Shopping list is empty!')
    else:
        formatted_list = '\n- '.join(SHOPPING_LIST)

        # escape especial characters to avoid markdown errors
        formatted_list = re.sub(r"([().-])", r"\\\1", formatted_list)
        update.message.reply_markdown_v2(f'*Shopping list:*\n\- {formatted_list}')


def add(update: Update, context: CallbackContext) -> None:
    """Add item to shopping list with /add."""
    global SHOPPING_LIST

    global LIST_BACKUP
    LIST_BACKUP = SHOPPING_LIST.copy()

    items = ' '.join(context.args).strip().split(',')

    for item in items:
        if len(item) > 0:
            item = item.strip().title()
            SHOPPING_LIST.append(item)
            update.message.reply_text(f'"{item}" added to shopping list.')
        else:
            update.message.reply_text('Please specify an item to add. For example: /add milk, eggs, bread')



def remove(update: Update, context: CallbackContext) -> None:
    """Display shopping list when /remove is issued."""
    global SHOPPING_LIST

    global LIST_BACKUP
    LIST_BACKUP = SHOPPING_LIST.copy()

    item = ' '.join(context.args).strip()

    if len(item) > 0:
        for element in SHOPPING_LIST:
            if item.lower() in element.lower():
                SHOPPING_LIST.remove(element)
                update.message.reply_text(f'"{element}" removed from shopping list.')
                return
    else:
        update.message.reply_text('Please specify an item to remove. For example: /remove milk')

def clear(update: Update, context: CallbackContext) -> None:
    """Clear shopping list with /clear."""
    # update.message.reply_text('Are you sure?', reply_markup=ForceReply(selective=True))
    global SHOPPING_LIST

    global LIST_BACKUP
    LIST_BACKUP = SHOPPING_LIST

    SHOPPING_LIST = list()
    update.message.reply_text('List cleared!')


def undo(update: Update, context: CallbackContext) -> None:
    """Undo last action."""
    global SHOPPING_LIST
    global LIST_BACKUP
    
    # restore from backup
    SHOPPING_LIST = LIST_BACKUP

    update.message.reply_text('Shopping list restored.')
    show_list(update, context)


def help(update: Update, context: CallbackContext) -> None:
    """Show list of commands when the command /help is issued."""
    message = '''List of commands:
/list - Show products in the shopping list
/add - Add product to the shopping list
/remove - Remove a product from the shopping list
/clear - Remove all products from the shopping list'''
    update.message.reply_text(message)


def main() -> None:
    """Start the bot. Pressing Ctrl-C or receiving a SIGINT, SIGTERM 
    or SIGABRT will trigger the shutdown function."""
    global updater

    restore_from_backup()
    signal.signal(signal.SIGINT, shutdown)

    # Create the Updater and pass it your bot's token.
    try:
        updater = Updater(os.environ.get('TELEGRAM_API_KEY'))
    except ValueError:
        logger.error('No Telegram API key found!')
        return

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("list", show_list))
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("remove", remove))
    dispatcher.add_handler(CommandHandler("clear", clear))
    dispatcher.add_handler(CommandHandler("undo", undo))

    # Start the Bot
    updater.start_polling()


if __name__ == '__main__':
    main()
