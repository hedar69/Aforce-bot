import os
import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from binance.client import Client

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

# Binance client setup
binance_client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)

# Security setup
SECRET_CODE = "gefmiz-Dapbyt-5cejgu"
AUTHORIZED_USERS = set()

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in AUTHORIZED_USERS:
        await update.message.reply_text("أهلاً بك مجددًا في AFORCE! أرسل /scan لتحليل السوق.")
    else:
        await update.message.reply_text("مرحبًا بك في AFORCE!\nالرجاء إدخال رمز الدخول:")

# Code verification
async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text.strip()

    if user_id in AUTHORIZED_USERS:
        return

    if message == SECRET_CODE:
        AUTHORIZED_USERS.add(user_id)
        await update.message.reply_text("تم التفعيل! أرسل /scan لتحصل على التحليل.")
    else:
        await update.message.reply_text("رمز خاطئ، حاول مرة أخرى.")

# Scan command (smart analysis)
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in AUTHORIZED_USERS:
        await update.message.reply_text("أرسل رمز الدخول أولاً.")
        return

    coin = "BTCUSDT"
    try:
        data = binance_client.get_ticker(symbol=coin)
        price = float(data['lastPrice'])
    except:
        price = round(random.uniform(50000, 65000), 2)

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
        f"العملة: BTC\n"
        f"السعر الحالي: {price} USDT\n"
        f"حركة السعر: {price_move}%\n"
        f"تحرك الحيتان: {whale_action}\n"
        f"الخبر المؤثر: {news}\n"
        f"نقاط التقييم: {score}/5\n"
        f"النتيجة: {recommendation}"
    )
    await update.message.reply_text(msg)

# Fake /deal command
async def deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in AUTHORIZED_USERS:
        await update.message.reply_text("أرسل رمز الدخول أولاً.")
        return

    await update.message.reply_text("صفقة جديدة:\nالعملة: OP\nسعر الدخول: 2.20\nالمضاعف: x5\nالبيع عند: 2.68\nالوقت المتوقع: 45 دقيقة")

# Fake /market command
async def market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in AUTHORIZED_USERS:
        await update.message.reply_text("أرسل رمز الدخول أولاً.")
        return

    await update.message.reply_text("حركة غير طبيعية على عملة PEPE\nكمية ضخمة دخلت خلال دقائق!")

# Build bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("scan", scan))
app.add_handler(CommandHandler("deal", deal))
app.add_handler(CommandHandler("market", market))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_code))

app.run_polling()
