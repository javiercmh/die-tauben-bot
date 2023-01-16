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

Create a virtual environment and install the requirements.

    $ pip install -r requirements.txt

Finally, paste the API key in `api.key`.

Run `run_bot.sh`.