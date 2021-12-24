from flask import Flask, request
import os
import logging
import telegram
import time
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

#locales
from telebot.credentials import bot_token, bot_user_name,URL
from telebot.mastermind import get_response
#global bot
global TOKEN
TOKEN = bot_token
#bot = telegram.Bot(token=TOKEN)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger("test")
#herokuname = "name"
#PORT = int(os.environ.get('PORT', '8443'))
updater = Updater(TOKEN, use_context=True)
bot = updater.bot
update_queue = updater.update_queue
dispatcher = updater.dispatcher

app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = telegram.update.Update.de_json(request.get_json(force=True), bot)
    logger.info(f"update id is : {update.update_id}")
    update_queue.put(update)
    return 'OK'


def start(update:Update, context:CallbackContext):
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



@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    dispatcher.add_handler(CommandHandler("start", start))
    updater._init_thread(dispatcher.start, "dispatcher")
    
    #teniamos bot.setWebhook pero cambiamos a set_webhook porque los bot se 
    #declaran diferente en este ejemplo, aqui es a partir del updater en el otro es de telegram
    bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    #bot.set_webhook(f"https://{herokuname}.herokuapp.com/{TOKEN}")

    time.sleep(5)
    # note the threaded arg which allow
    # your app to have more than one thread
    app.run(threaded=True)
    
