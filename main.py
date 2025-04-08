import telegram
from telegram.ext import Updater, CommandHandler
import logging

TOKEN = "7830664951:AAF9qMrWA1ayIqCj3os9tGRpAnA1E5rKyDI"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    user = update.effective_user.first_name
    update.message.reply_text(f"أهلاً {user}! البوت شغال رسميًا، توصيات AFORCE رح توصلك هون لحظة بلحظة.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
