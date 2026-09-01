from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# កូដពេលចាប់ផ្តើម /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🛍️ សេវាកម្ម", "ទំនាក់ទំនង (Contact)"],
        ["ព័ត៌មាន (About)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("សួស្តី! សូមជ្រើសរើសជម្រើសខាងក្រោម៖", reply_markup=reply_markup)

# កូដពេលអ្នកប្រើប្រាស់ចុច Menu នៅខាងក្រោម
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "🛍️ សេវាកម្ម":
        inline_keyboard = [
            [InlineKeyboardButton("Facebook", callback_data="menu_facebook")],
            [InlineKeyboardButton("TikTok", callback_data="menu_tiktok")]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await update.message.reply_text("សូមជ្រើសរើសប្រភេទសេវាកម្មខាងក្រោម៖", reply_markup=reply_markup)
        
    elif text == "ទំនាក់ទំនង (Contact)":
        await update.message.reply_text("នេះគឺជាឆាតទំនាក់ទំនងរបស់យើង។")
        
    elif text == "ព័ត៌មាន (About)":
        await update.message.reply_text("នេះគឺជា Bot បម្រើសេវាកម្មផ្សេងៗ។")

# កូដពេលអ្នកប្រើប្រាស់ចុចលើប៊ូតុង Inline
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "menu_facebook":
        fb_keyboard = [
            [InlineKeyboardButton("FACEBOOK FOLLOW", callback_data="fb_follow")],
            [InlineKeyboardButton("FACEBOOK LIKE", callback_data="fb_like")],
            [InlineKeyboardButton("FACEBOOK VIEWS", callback_data="fb_views")]
        ]
        reply_markup = InlineKeyboardMarkup(fb_keyboard)
        await query.message.edit_text("សូមជ្រើសរើសសេវាកម្ម Facebook ៖", reply_markup=reply_markup)
        
    elif query.data == "menu_tiktok":
        await query.message.edit_text("សេវាកម្ម TikTok កំពុងរៀបចំ...")
        
    elif query.data == "fb_follow":
        # បង្កើត Button តម្លៃតម្រៀបចុះក្រោមស្អាតដូចក្នុងរូប
        price_keyboard = [
            [InlineKeyboardButton("1K ~ 0.69$", callback_data="buy_1k")],
            [InlineKeyboardButton("5K ~ 4.5$", callback_data="buy_5k")],
            [InlineKeyboardButton("10K ~ 8.60$", callback_data="buy_10k")]
        ]
        reply_markup = InlineKeyboardMarkup(price_keyboard)
        await query.message.edit_text("📌 សូមជ្រើសរើសកញ្ចប់ FACEBOOK FOLLOW ៖", reply_markup=reply_markup)
        
    elif query.data == "fb_like":
        await query.message.edit_text("អ្នកបានជ្រើសរើស៖ FACEBOOK LIKE")
    elif query.data == "fb_views":
        await query.message.edit_text("អ្នកបានជ្រើសរើស៖ FACEBOOK VIEWS")
        
    elif query.data in ["buy_1k", "buy_5k", "buy_10k"]:
        package = query.data.replace("buy_", "").upper()
        await query.message.edit_text(f"អ្នកបានជ្រើសរើសកញ្ចប់ {package}។ សូមផ្ញើតំណរ (Link) មកទីនេះដើម្បីបន្ត!")

if __name__ == "__main__":
    TOKEN = "8675478122:AAFem3pCVLz_zZBebYuRmWcKGFAR1FBGY5Y"
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    print("Bot កំពុងដំណើរការ...")
    app.run_polling()
