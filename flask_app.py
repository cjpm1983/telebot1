from flask import Flask, request
import os
import logging
import telegram
import time
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater, MessageHandler

#locales
from telebot.credentials import bot_token, bot_user_name,URL
from telebot.mastermind import get_response
global bot
global TOKEN
TOKEN = bot_token
#bot = telegram.Bot(token=TOKEN)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger("test")
#herokuname = "name"
PORT = int(os.environ.get('PORT', '8443'))
global updater
updater = Updater(TOKEN, use_context=True)
bot = updater.bot

global update_queue
global dispatcher
update_queue = updater.update_queue
dispatcher = updater.dispatcher

app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = telegram.update.Update.de_json(request.get_json(force=True), bot)
    logger.info(f"update id is : {update.update_id}")
    texto = update.message.text.encode('utf-8').decode()
    logger.info(f"el texto es : {texto}")
    update_queue.put(update)
    return 'OK'


def start(update:Update, context:CallbackContext):
    #msg_id = update.message.message_id
    update.message.reply_text("ok")


#eSTE ultimo ejemplo no incluye esta funcionsino que llama setwebhook 
#en elmain, lodejamos pues no debe de dar conflicto
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


def echo(update, context):
   texto = update.message.text.encode('utf-8').decode()
   logger.info("ha entrado con %s" % (texto))
   #context.bot.send_message(chat_id = update.effective_chat.id, text = update.message.text)
   context.bot.send_message(chat_id = update.effective_chat.id, text = texto)
   bot.send_message(chat_id=update.message.chat_id, text=texto)

#@app.route('/')
#def index():
#    return '.'


if __name__ == '__main__':

    #logger.info("------Entramos al MAIN --------")

    dispatcher.add_handler(CommandHandler("start", start))
    
    #echo_handler = MessageHandler(Filters.all, echo)
    echo_handler = MessageHandler("lll", echo)
    updater.dispatcher.add_handler(echo_handler)
    
    updater._init_thread(dispatcher.start, "dispatcher")
#teniamos bot.setWebhook pero cambiamos a set_webhook porque los bot se 
    #declaran diferente en este ejemplo, aqui es a partir del updater en el otro es de telegram
    bot.set_webhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    #bot.set_webhook(f"https://{herokuname}.herokuapp.com/{TOKEN}")

    time.sleep(5)
    # note the threaded arg which allow
    # your app to have more than one thread
    #app.run(threaded=True)
    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=True
    )
    
    
