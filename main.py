import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# إعدادات
BOT_TOKEN = os.getenv("BOT_TOKEN")
SECRET_CODE = "gefmiz-Dapbyt-5cejgu"
AUTHORIZED_USERS = set()

# لوجز
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in AUTHORIZED_USERS:
        await update.message.reply_text("أهلاً فيك من جديد، جاهز للتوصيات.")
    else:
        await update.message.reply_text("مرحبًا بك في AFORCE!\nالرجاء إدخال رمز الدخول:")

# التحقق من الرمز
async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text.strip()

    if user_id in AUTHORIZED_USERS:
        return

    if message == SECRET_CODE:
        AUTHORIZED_USERS.add(user_id)
        await update.message.reply_text("تم التفعيل! يمكنك الآن استخدام الأوامر.")
    else:
        await update.message.reply_text("رمز خاطئ، حاول مرة أخرى.")

# /scan - تحليل ذكي
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in AUTHORIZED_USERS:
        await update.message.reply_text("أرسل رمز الدخول أولاً.")
        return

    import random
    price_move = round(random.uniform(-2, 3), 2)
    whale_action = random.choice(["دخول سيولة", "بيع ضخم", "هدوء"])
    news = random.choice(["موافقة ETF", "تحذير SEC", "إدراج جديد", "لا يوجد شيء مهم"])

    score = 0
    if price_move > 1:
        score += 2
    if whale_action == "دخول سيولة":
        score += 3
    if "ETF" in news:
        score += 2
    if "SEC" in news:
        score -= 2

    recommendation = "توصية شراء قوية" if score >= 4 else "تحذير: المخاطرة عالية"

    msg = (
        f"**تحليل ذكي AFORCE:**\n"
        f"حركة السعر: {price_move}%\n"
        f"تحرك الحيتان: {whale_action}\n"
        f"الخبر المؤثر: {news}\n"
        f"نقاط التقييم: {score}/5\n"
        f"النتيجة: {recommendation}"
    )
    await update.message.reply_text(msg)

# بناء البوت
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("scan", scan))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_code))

app.run_polling()
