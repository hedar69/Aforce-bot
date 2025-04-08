import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")
SECRET_CODE = "gefmiz-Dapbyt-5cejgu"

# تخزين المستخدمين المصرح لهم
authorized_users = set()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in authorized_users:
        await update.message.reply_text("أهلًا من جديد! جاهز للتوصيات.")
    else:
        await update.message.reply_text("أهلاً! الرجاء إرسال رمز الدخول للمتابعة.")

async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id in authorized_users:
        await update.message.reply_text("أنت مصرح مسبقًا.")
        return

    if text == SECRET_CODE:
        authorized_users.add(user_id)
        await update.message.reply_text("تم التحقق! مرحبًا بك في Aforce Bot.")
    else:
        await update.message.reply_text("رمز الدخول غير صحيح!")

async def secret_area(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in authorized_users:
        await update.message.reply_text("هاي منطقة خاصة... التوصيات راح توصلك هون!")
    else:
        await update.message.reply_text("أنت غير مصرح لك. أرسل رمز الدخول أولاً.")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_code))
app.add_handler(CommandHandler("deal", secret_area))  # أمر لتجريب إرسال توصية سرية

app.run_polling()
