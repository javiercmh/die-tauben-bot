#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import re

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
SHOPPING_LIST = list()
LIST_BACKUP = SHOPPING_LIST

def get_token():
    """Get the bot token from file."""
    with open('api.key') as f:
        return f.read().strip()


# Define a few command handlers. These usually take the two arguments update and
# context.
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
            update.message.reply_text('Please specify an item to add.')



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
        update.message.reply_text('Please specify an item to remove.')

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


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(get_token())

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

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
