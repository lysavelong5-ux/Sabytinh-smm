from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# កូដពេលចាប់ផ្តើម /start បង្ហាញ Reply Keyboard ខាងក្រោម
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🛍️ សេវាកម្ម", "ទំនាក់ទំនង (Contact)"],
        ["ព័ត៌មាន (About)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("សួស្តី! សូមជ្រើសរើសជម្រើសខាងក្រោម៖", reply_markup=reply_markup)

# កូដពេលអ្នកប្រើប្រាស់ចុចលើប៊ូតុងណាមួយនៅខាងក្រោម
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # បើចុចចំពាក្យ 🛍️ សេវាកម្ម
    if text == "🛍️ សេវាកម្ម":
        inline_keyboard = [
            [InlineKeyboardButton("Facebook", url="https://www.facebook.com")],
            [InlineKeyboardButton("TikTok", url="https://www.tiktok.com")]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await update.message.reply_text("សូមជ្រើសរើសវេបសាយខាងក្រោម៖", reply_markup=reply_markup)
        
    elif text == "ទំនាក់ទំនង (Contact)":
        await update.message.reply_text("นี่คือช่องทางติดต่อเรา: Telegram / Phone")
        
    elif text == "ព័ត៌មាន (About)":
        await update.message.reply_text("นี่คือ Bot สำหรับให้บริการต่างๆ ของเรา។")

if __name__ == "__main__":
    TOKEN = "8675478122:AAFem3pCVLz_zZBebYuRmWcKGFAR1FBGY5Y"
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot កំពុងដំណើរការ...")
    app.run_polling()
