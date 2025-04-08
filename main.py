import os
import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
AUTHORIZED_USERS = set()
SECRET_CODE = "gefmiz-Dapbyt-5cejgu"

logging.basicConfig(level=logging.INFO)

# تحليل داخلي وهمي (مثال)
def internal_analysis():
    prices = random.uniform(-2, 3)  # حركة سعر
    whales = random.choice(["دخول سيولة", "بيع ضخم", "هدوء"])
    news = random.choice(["ETF موافقة", "تحذير SEC", "لا شيء مهم"])
    
    score = 0
    if prices > 1: score += 2
    if whales == "دخول سيولة": score += 3
    if "ETF" in news: score += 2
    if "SEC" in news: score -= 2
    
    recommendation = "توصية شراء" if score >= 4 else "انتبه: مخاطرة"
    
    return {
        "الحركة": f"{prices:.2f}%",
        "الحيتان": whales,
        "الخبر": news,
        "التقييم": score,
        "النتيجة": recommendation
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in AUTHORIZED_USERS:
        await update.message.reply_text("أهلاً من جديد، جاهز للتوصيات.")
    else:
        await update.message.reply_text("من فضلك أرسل رمز الدخول:")

async def check_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    if text == SECRET_CODE:
        AUTHORIZED_USERS.add(user_id)
        await update.message.reply_text("تم التفعيل، يمكنك الآن استخدام البوت.")
    elif user_id not in AUTHORIZED_USERS:
        await update.message.reply_text("رمز خاطئ، حاول مرة أخرى.")

async def insight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in AUTHORIZED_USERS:
        await update.message.reply_text("أنت غير مصرح. أرسل الرمز أولًا.")
        return
    
    data = internal_analysis()
    msg = (
        f"**تحليل ذكي AFORCE:**\n"
        f"حركة السعر: {data['الحركة']}\n"
        f"تحرك الحيتان: {data['الحيتان']}\n"
        f"الخبر المؤثر: {data['الخبر']}\n"
        f"نقاط التقييم: {data['التقييم']}/5\n"
        f"النتيجة: {data['النتيجة']}"
    )
    await update.message.reply_text(msg)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("scan", insight))
app.add_handler(CommandHandler("code", check_code))
app.add_handler(CommandHandler("check", check_code))  # fallback للرسالة كرمز

app.run_polling()
