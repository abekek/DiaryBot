import constants
import telegram
import datetime
import time
import sqlite3
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from dbhelper import DBHelper
from functools import wraps
from telegram import ChatAction
import logging
updater = Updater(token=constants.TOKEN)

dispatcher = updater.dispatcher

#db = DBHelper()
#conn = sqlite3.connect("notes.db")
#cursor = conn.cursor()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id , action = telegram.ChatAction.TYPING)
    time.sleep(1)
    bot.send_message(chat_id=update.message.chat_id, text="Write your thoughts below!")

def help(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id , action = telegram.ChatAction.TYPING)
    time.sleep(.500)
    bot.send_message(chat_id=update.message.chat_id, text="I will help you!")

def echo(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id , action = telegram.ChatAction.TYPING)
    time.sleep(1)
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
    #db.add_item(chat.id=update.message.chat_id, text=update.message.text)
    
def send_action(action):
    def decorator(func):
        @wraps(func)
        def command_func(*args, **kwargs):
            bot, update = args
            bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(bot, update, **kwargs)
        return command_func
    
    return decorator

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(CommandHandler("help", help))

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

#hashtag_handler = MessageHandler(Filters.caption_entity("hashtag"), start)
#dispatcher.add_handler(hashtag_handler)

updater.start_polling()