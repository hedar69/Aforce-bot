import os
import telegram
from telegram.ext import Updater, CommandHandler
import logging

# استخدم المتغير البيئي بدل التوكن المباشر
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    user = update.effective_user.first_name
    update.message.reply_text(f"أهلاً {user}! البوت شغال رسميّاً.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()