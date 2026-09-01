from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Dictionary សម្រាប់រក្សាទុកកញ្ចប់ដែលអតិថិជនបានជ្រើសរើសបណ្តោះអាសន្ន
user_selected_package = {}

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
    user_id = update.effective_user.id
    
    # ពិនិត្យមើលថាតើអតិថិជនកំពុងស្ថិតក្នុងដំណាក់កាលផ្ញើ Link ឬអត់
    if user_id in user_selected_package:
        package = user_selected_package[user_id]
        link = text
        
        # 1. ឆ្លើយតបប្រាប់អតិថិជនថារួចរាល់
        await update.message.reply_text("✅ អរគុណ! ការកុម្ម៉ង់របស់អ្នកត្រូវបានបញ្ជូនទៅកាន់ Admin រួចរាល់ហើយ។ សូមរង់ចាំបន្តិច!")
        
        # 2. ផ្ញើព័ត៌មានលម្អិត (កញ្ចប់ + Link + ព័ត៌មានអតិថិជន) ចូលទៅក្នុង Group ORDER
        GROUP_CHAT_ID = "-1003950979639"
        user = update.effective_user
        notification_text = (
            "🔔 **មានការបញ្ជាទិញថ្មី!**\n\n"
            f"• សេវាកម្ម: FACEBOOK FOLLOW ({package})\n"
            f"• តំណរ (Link): {link}\n"
            f"• អតិថិជន: {user.first_name} (@{user.username if user.username else 'គ្មាន'})\n"
            f"• User ID: {user.id}"
        )
        try:
            await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=notification_text, parse_mode="Markdown")
        except Exception as e:
            print(f"Error sending notification: {e}")
            
        # លុប State ចេញវិញក្រោយពេលបញ្ជូនរួច
        del user_selected_package[user_id]
        return

    #  xử lý เมนู ปกติ
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
    user_id = query.from_user.id
    
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
        
        # កត់ត្រាទុកថាសមាជិកនេះបានជ្រើសរើសកញ្ចប់ណា
        user_selected_package[user_id] = f"FACEBOOK FOLLOW ({package})"
        
        # ឱ្យអតិថិជនផ្ញើ Link ចូលមក
        await query.message.edit_text(f"អ្នកបានជ្រើសរើសកញ្ចប់ **{package}** ហើយ។\n\n🔗 សូមផ្ញើតំណរ (Link) ហ្វេសប៊ុករបស់អ្នកមកទីនេះឥឡូវនេះ!")

if __name__ == "__main__":
    TOKEN = "8675478122:AAFem3pCVLz_zZBebYuRmWcKGFAR1FBGY5Y"
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    print("Bot កំពុងដំណើរការ...")
    app.run_polling()
