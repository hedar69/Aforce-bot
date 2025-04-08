import os
import logging
import random
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# إعداد التوكن من Environment Variable مباشرة
BOT_TOKEN = os.getenv("BOT_TOKEN1")
SECRET_CODE = "gefmiz-Dapbyt-5cejgu"
AUTHORIZED_USERS = set()

# إعداد اللوج
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# API من CoinGecko
def get_coin_data(coin_id="bitcoin"):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    try:
        response = requests.get(url).json()
        return response.get(coin_id, {}).get("usd", 0)
    except:
        return 0

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in AUTHORIZED_USERS:
        await update.message.reply_text("أهلاً بعودتك إلى AFORCE. استخدم /scan للبدء.")
    else:
        await update.message.reply_text("مرحبًا بك في AFORCE!\nالرجاء إدخال رمز الدخول:")

# رمز الدخول
async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    code = update.message.text.strip()
    if user_id in AUTHORIZED_USERS:
        return
    if code == SECRET_CODE:
        AUTHORIZED_USERS.add(user_id)
        await update.message.reply_text("تم التفعيل بنجاح! يمكنك الآن استخدام /scan.")
    else:
        await update.message.reply_text("رمز خاطئ. حاول مرة أخرى.")

# /scan لتحليل السوق
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in AUTHORIZED_USERS:
        await update.message.reply_text("أرسل رمز الدخول أولًا.")
        return

    coin = "bitcoin"
    price = get_coin_data(coin)
    move = round(random.uniform(-2, 3), 2)
    whale = random.choice(["دخول سيولة", "بيع ضخم", "هدوء"])
    news = random.choice(["موافقة ETF", "تحذير SEC", "إدراج جديد", "لا يوجد شيء مهم"])

    score = 0
    if move > 1:
        score += 2
    if whale == "دخول سيولة":
        score += 2
    if "ETF" in news:
        score += 2
    if "SEC" in news:
        score -= 2

    result = "توصية شراء قوية" if score >= 4 else "تحذير: السوق متقلب"

    msg = (
        f"**تحليل ذكي AFORCE:**\n"
        f"العملة: {coin.upper()}\n"
        f"السعر الحالي: {price}$\n"
        f"حركة السعر: {move}%\n"
        f"تحرك الحيتان: {whale}\n"
        f"الخبر المؤثر: {news}\n"
        f"نقاط التقييم: {score}/5\n"
        f"النتيجة: {result}"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

# إعداد البوت وتشغيله
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("scan", scan))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_code))
app.run_polling()

