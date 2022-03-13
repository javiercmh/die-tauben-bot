# Die Tauben Bot

Simple Telegram bot to manage a shopping list.

List of commands:
/list - Show products in the shopping list
/add - Add product to the shopping list
/remove - Remove a product from the shopping list
/clear - Remove all products from the shopping list
/undo - Undo last action

Press Ctrl-C on the command line or send a signal to the process to stop the
bot.

## Installing

First I recommend creating a virtual environment.
Then you need to install the following library:

    $ pip install python-telegram-bot --upgrade

Finally, put your API key in a file called `api.key`.

You are ready to run the Python file.