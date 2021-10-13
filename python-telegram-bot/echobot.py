import logging
from telegram import Bot
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters

TOKEN="<-YOUR TOKEN HERE->"
bot = Bot(token=TOKEN)

def start_command(update,context):
    user_id = update.effective_user.id
    bot.send_message(chat_id=user_id,text="Hey there\nI'm blogtest19\n")

def echo_message(update,context):
    user_id = update.effective_user.id
    message = update.message.text
    bot.send_message(chat_id=user_id,text=message)

def main():
    updater=Updater(token=TOKEN,use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start_command))
    dp.add_handler(MessageHandler(filters=Filters.all,callback=echo_message))
    updater.start_polling()

if __name__ == "__main__":
    main()
