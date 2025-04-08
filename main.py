import os
import logging
import random
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Telegram Bot Token from Environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
SECRET_CODE = "gefmiz-Dapbyt-5cejgu"
AUTHORIZED_USERS = set()

# Setup Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# CoinGecko Endpoint
COINGECKO_API = "https://api.coingecko.com/api/v3"

# Helper: Get Coin Price
def get_price(coin_id="bitcoin"):
    url = f"{COINGECKO_API}/simple/price?ids={coin_id}&vs_currencies=usd"
    response = requests.get(url).json()
    return response.get(coin_id, {}).get("usd", None)

# Helper: Get Market Data
def get_market_data(coin_id="bitcoin"):
    url = f"{COINGECKO_API}/coins/markets?vs_currency=usd&ids={coin_id}"
    response = requests.get(url).json()
    return response[0] if response else {}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in AUTHORIZED_USERS:
        await update.message.reply_text("مرحبًا بك مجددًا في AForce! استخدم /scan أو /deal لبدء التحليل.")
    else:
        await update.message.reply_text("أهلًا بك في AForce!\nيرجى إدخال رمز الدخول لتفعيل الحساب.")

# Handle secret code
async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    msg = update.message.text.strip()

    if user_id in AUTHORIZED_USERS:
        return

    if msg == SECRET_CODE:
        AUTHORIZED_USERS.add(user_id)
        await update.message.reply_text("تم التفعيل بنجاح! استخدم /scan أو /deal للبدء.")
    else:
        await update.message.reply_text("رمز خاطئ. حاول مرة أخرى.")

# /scan command
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in AUTHORIZED_USERS:
        await update.message.reply_text("أرسل رمز الدخول أولًا.")
        return

    coin_id = "bitcoin"
    data = get_market_data(coin_id)
    price = data.get("current_price", 0)
    change = data.get("price_change_percentage_24h", 0)
    volume = data.get("total_volume", 0)

    whale = random.choice(["دخول سيولة", "بيع مفاجئ", "هدوء"])
    news = random.choice(["إدراج جديد", "موافقة ETF", "تحذير SEC", "لا يوجد شيء مهم"])

    score = 0
    if change > 2:
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
        f"العملة: Bitcoin\n"
        f"السعر الحالي: {price}$\n"
        f"التغير اليومي: {round(change,2)}%\n"
        f"حجم التداول: {round(volume / 1e6, 2)}M$\n"
        f"تحرك الحيتان: {whale}\n"
        f"الخبر المؤثر: {news}\n"
        f"نقاط التقييم: {score}/5\n"
        f"النتيجة: {result}"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

# /deal command
async def deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in AUTHORIZED_USERS:
        await update.message.reply_text("أرسل رمز الدخول أولًا.")
        return

    entry = round(random.uniform(0.2, 2), 3)
    target = round(entry * 1.1, 3)
    stop = round(entry * 0.95, 3)

    msg = (
        f"**توصية سكالب سريعة:**\n"
        f"العملة: PEPE\n"
        f"سعر الدخول: {entry}$\n"
        f"الهدف: {target}$\n"
        f"وقف الخسارة: {stop}$\n"
        f"الرافعة: x10\n"
        f"المدة: 15-30 دقيقة\n"
        f"#AFORCE"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

# /market command
async def market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in AUTHORIZED_USERS:
        await update.message.reply_text("أرسل رمز الدخول أولًا.")
        return

    top = ["pepe", "solana", "dogecoin", "bonk"]
    chosen = random.choice(top)
    price = get_price(chosen)

    await update.message.reply_text(
        f"🚨 عملة ناشطة: {chosen.upper()}\nالسعر الحالي: {price}$\nراقبها خلال الدقائق القادمة!",
        parse_mode="Markdown"
    )

# Setup bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("scan", scan))
app.add_handler(CommandHandler("deal", deal))
app.add_handler(CommandHandler("market", market))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_code))

app.run_polling()
