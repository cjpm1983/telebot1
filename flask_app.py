
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request

import telegram
import logging
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext

from telebot.credentials import bot_token, bot_user_name,URL
from telebot.mastermind import get_response

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger("test")

#from telegram.ext import (Updater, CommandHandler)

app = Flask(__name__)

#@app.route('/')
#def hello_world():
#    return 'Hello from Flask!'

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    #updatet = telegram.Update
    #query = updatet.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    #query.answer()
    #updater = Updater(TOKEN)

    #updater.dispatcher.add_handler(CallbackQueryHandler(button))
    
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    logger.info(f"update id is : {update}")
    chat_id=-1
    msg_id=-1
    text = ""
    bundle = {}
    if (update.callback_query):
        chat_id = update.callback_query.message.chat.id
        msg_id = update.callback_query.message.message_id
        text = update.callback_query.data.encode('utf-8').decode()
        
    else:
       chat_id = update.message.chat.id
       msg_id = update.message.message_id
       text = update.message.text.encode('utf-8').decode()

    bundle = get_response(text)
    print("got text message :", text)
# here we call our super AI
    '''
    markup = {'inline_keyboard': [[{'text': 'Gn', 'callback_data': 'Return value 1'},
             {'text': 'Mt', 'callback_data': 'Return value 2'}]]}
    if text == '/start':
        bot.sendMessage (chat_id=chat_id, text=str("Hi! Which one do you want? choose from the below keyboard buttons."), reply_markup=markup)
        bot.sendMessage(chat_id=chat_id, text=str(now.hour)+str(":")+str(now.minute))
        return 'ok'
    '''
    #logger.info(f"update id is : {update}")

    #bundle = get_response(text)
# now just send the message back
    # notice how we specify the chat and the msg we reply to
    #bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)
    response = bundle["txt"]
    if len(response) > 4096:
       for x in range(0, len(response), 4096):
          bot.send_message(chat_id=chat_id, text=response[x:x+4096])
    else:
       bot.send_message(chat_id=chat_id, text=response)

    if "btns" in bundle.keys():
       btns = bundle["btns"]
       bot.sendMessage (chat_id=chat_id, text=str("------------------"), reply_markup=btns)
    
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
