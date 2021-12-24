
# A very simple Flask Hello World app for you to get started with...
#con handlers
from flask import Flask, request

import telegram


from telebot.credentials import bot_token, bot_user_name,URL
from telebot.mastermind import get_response

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

#from telegram.ext import (Updater, CommandHandler)

app = Flask(__name__)

#@app.route('/')
#def hello_world():
#    return 'Hello from Flask!'

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():

    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    echo_handler = MessageHandler(Filters.text), echo)
    updater.dispatcher.add_handler(echo_handler)
    
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)
# get the chat_id to be able to respond to the same user
    chat_id = update.message.chat.id
    # get the message id to be able to reply to this specific message
    msg_id = update.message.message_id
# Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)
# here we call our super AI

    '''    
    bundle = get_response(text)

    response = bundle["txt"]
    if len(response) > 4096:
       for x in range(0, len(response), 4096):
          bot.send_message(chat_id=chat_id, text=response[x:x+4096])
    else:
       bot.send_message(chat_id=chat_id, text=response)

    if "btns" in bundle.keys():
       btns = bundle["btns"]
       #bot.sendMessage (chat_id=chat_id, text=str("---"), reply_markup=btns)
    '''
    return 'ok'


def button(update: telegram.Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
    # note the threaded arg which allow
    # your app to have more than one thread
    app.run(threaded=True)
