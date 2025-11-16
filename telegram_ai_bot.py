import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# ============================================
# 🔧 تنظیمات - این قسمت را پر کنید
# ============================================

# توکن ربات تلگرام شما (از @BotFather دریافت کنید)
TELEGRAM_BOT_TOKEN = "8358065838:AAH769yiegztjRB7OG2XYfiNTTtv_2V8Bq4"

# آی‌پی یا آدرس سرویس هوش مصنوعی شما (مثال: "http://192.168.1.100:8000" یا "https://api.example.com")
AI_SERVICE_IP = ""
# مسیر endpoint هوش مصنوعی (معمولاً "/chat" یا "/api/chat" - اگر می‌دانید تغییر دهید)
AI_ENDPOINT = "/chat"  # می‌توانید این را هم تغییر دهید

# ============================================
# تنظیمات لاگ
# ============================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============================================
# توابع ربات
# ============================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /start - خوش‌آمدگویی"""
    welcome_message = (
        "🤖 سلام! به ربات هوش مصنوعی خوش آمدید\n\n"
        "💬 می‌توانید هر سوالی بپرسید و ربات به شما پاسخ می‌دهد.\n\n"
        "📌 دستورات:\n"
        "/start - نمایش این پیام\n"
        "/help - راهنمای استفاده"
    )
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /help - راهنما"""
    help_text = (
        "📚 راهنمای استفاده:\n\n"
        "1️⃣ برای گفتگو با هوش مصنوعی:\n"
        "   فقط پیام خود را بنویسید و ارسال کنید\n\n"
        "2️⃣ ربات پیام شما را به سرویس هوش مصنوعی ارسال می‌کند\n"
        "   و پاسخ را برایتان برمی‌گرداند\n\n"
        "3️⃣ دستورات:\n"
        "   • /start - شروع\n"
        "   • /help - راهنمایی\n\n"
        "⚠️ اگر مشکلی پیش آمد، بررسی کنید:\n"
        "   - آی‌پی سرویس هوش مصنوعی درست تنظیم شده باشد\n"
        "   - سرویس هوش مصنوعی در دسترس باشد"
    )
    await update.message.reply_text(help_text)

def call_ai_service(message_text: str) -> str:
    """
    ارسال پیام به سرویس هوش مصنوعی و دریافت پاسخ
    
    این تابع با سرویس AI شما ارتباط برقرار می‌کند.
    اگر سرویس شما فرمت خاصی نیاز دارد، این تابع را تغییر دهید.
    """
    try:
        # ساخت URL کامل
        if not AI_SERVICE_IP.startswith("http"):
            # اگر IP بدون http است، اضافه می‌کنیم
            url = f"http://{AI_SERVICE_IP}{AI_ENDPOINT}"
        else:
            url = f"{AI_SERVICE_IP}{AI_ENDPOINT}"
        
        logger.info(f"ارسال درخواست به: {url}")
        
        # ارسال درخواست POST
        # فرمت درخواست: {"message": "متن پیام"}
        # اگر سرویس شما فرمت دیگری می‌خواهد، اینجا تغییر دهید
        payload = {
            "message": message_text,
            # می‌توانید فیلدهای دیگری اضافه کنید مثل:
            # "user_id": str(update.effective_user.id),
            # "language": "fa"
        }
        
        # ارسال درخواست
        response = requests.post(
            url,
            json=payload,
            timeout=30,  # 30 ثانیه timeout
            headers={
                "Content-Type": "application/json"
            }
        )
        
        logger.info(f"وضعیت پاسخ: {response.status_code}")
        
        # بررسی وضعیت پاسخ
        if response.status_code == 200:
            # اگر پاسخ موفق بود
            data = response.json()
            
            # تلاش برای خواندن پاسخ
            # فرمت پیش‌فرض: {"response": "پاسخ هوش مصنوعی"}
            # اگر سرویس شما فرمت دیگری دارد، اینجا تغییر دهید
            if isinstance(data, dict):
                # اگر پاسخ یک دیکشنری است
                if "response" in data:
                    return data["response"]
                elif "reply" in data:
                    return data["reply"]
                elif "text" in data:
                    return data["text"]
                elif "answer" in data:
                    return data["answer"]
                else:
                    # اگر هیچ کدام نبود، کل دیکشنری را برمی‌گرداند
                    return str(data)
            elif isinstance(data, str):
                # اگر پاسخ مستقیم رشته است
                return data
            else:
                return f"پاسخ دریافت شد: {str(data)}"
        
        else:
            # اگر خطا رخ داد
            error_msg = f"خطا: سرور پاسخ {response.status_code} داد"
            logger.error(f"{error_msg} - پاسخ: {response.text}")
            return f"❌ {error_msg}\n\nجزئیات: {response.text[:200]}"
    
    except requests.exceptions.ConnectionError:
        error_msg = "❌ نمی‌توانم به سرویس هوش مصنوعی متصل شوم"
        logger.error(f"{error_msg} - بررسی کنید آی‌پی درست باشد: {AI_SERVICE_IP}")
        return f"{error_msg}\n\n⚠️ لطفاً بررسی کنید:\n- آی‌پی سرویس درست باشد: {AI_SERVICE_IP}\n- سرویس در حال اجرا باشد"
    
    except requests.exceptions.Timeout:
        error_msg = "❌ زمان انتظار به پایان رسید (Timeout)"
        logger.error(error_msg)
        return f"{error_msg}\n\nسرویس هوش مصنوعی پاسخ نمی‌دهد. لطفاً دوباره تلاش کنید."
    
    except Exception as e:
        error_msg = f"❌ خطای غیرمنتظره: {str(e)}"
        logger.exception(error_msg)
        return f"{error_msg}\n\nلطفاً لاگ‌ها را بررسی کنید."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش پیام‌های متنی کاربر"""
    try:
        user_message = update.message.text
        
        # ارسال پیام "در حال پردازش"
        processing_msg = await update.message.reply_text("🤔 در حال پردازش...")
        
        # فراخوانی سرویس هوش مصنوعی
        ai_response = call_ai_service(user_message)
        
        # حذف پیام پردازش
        try:
            await processing_msg.delete()
        except:
            pass
        
        # ارسال پاسخ
        # تلگرام محدودیت 4096 کاراکتر دارد، اگر پاسخ طولانی باشد تقسیم می‌کنیم
        if len(ai_response) > 4096:
            # تقسیم به بخش‌های 4000 کاراکتری
            for i in range(0, len(ai_response), 4000):
                chunk = ai_response[i:i+4000]
                await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(ai_response)
    
    except Exception as e:
        logger.exception(f"خطا در پردازش پیام: {e}")
        await update.message.reply_text(
            "❌ خطایی در پردازش پیام رخ داد.\n"
            "لطفاً دوباره تلاش کنید یا بررسی کنید تنظیمات درست باشد."
        )

def main():
    """تابع اصلی برای راه‌اندازی ربات"""
    
    # بررسی تنظیمات
    if TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        logger.error("❌ لطفاً TELEGRAM_BOT_TOKEN را در فایل تنظیم کنید!")
        print("=" * 60)
        print("⚠️ خطا: توکن ربات تلگرام تنظیم نشده است!")
        print("لطفاً در فایل telegram_ai_bot.py متغیر TELEGRAM_BOT_TOKEN را پر کنید.")
        print("=" * 60)
        return
    
    if AI_SERVICE_IP == "YOUR_AI_SERVICE_IP_HERE":
        logger.error("❌ لطفاً AI_SERVICE_IP را در فایل تنظیم کنید!")
        print("=" * 60)
        print("⚠️ خطا: آی‌پی سرویس هوش مصنوعی تنظیم نشده است!")
        print("لطفاً در فایل telegram_ai_bot.py متغیر AI_SERVICE_IP را پر کنید.")
        print("=" * 60)
        return
    
    logger.info("=" * 60)
    logger.info("🚀 در حال راه‌اندازی ربات...")
    logger.info(f"📡 سرویس هوش مصنوعی: {AI_SERVICE_IP}{AI_ENDPOINT}")
    logger.info("=" * 60)
    
    # ساخت application تلگرام
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # اضافه کردن handler ها
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Handler برای پیام‌های متنی (غیر دستوری)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("✅ ربات آماده است و در حال گوش دادن...")
    print("\n✅ ربات راه‌اندازی شد!")
    print(f"📡 متصل به: {AI_SERVICE_IP}{AI_ENDPOINT}")
    print("برای توقف، Ctrl+C را فشار دهید.\n")
    
    try:
        # شروع polling
        application.run_polling(drop_pending_updates=True)
    except KeyboardInterrupt:
        logger.info("⏹️ ربات متوقف شد.")
        print("\n⏹️ ربات متوقف شد.")
    except Exception as e:
        logger.exception(f"❌ خطا در اجرای ربات: {e}")
        print(f"\n❌ خطا: {e}")

if __name__ == "__main__":
    main()
