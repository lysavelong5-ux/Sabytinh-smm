from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

user_states = {}

# កូដពេលចាប់ផ្តើម /start (ផ្ញើសារស្វាគមន៍សិន រួចបង្ហាញម៉ឺនុយ)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. ផ្ញើសារស្វាគមន៍ស្អាតៗ
    welcome_text = (
        "👋 សួស្តីស្វាគមន៍មកកាន់ប្រព័ន្ធបំរើសេវាកម្ម Social Media របស់យើង!\n\n"
        "✨ ទីនេះមានទទួលកុម្ម៉ង់សេវាកម្ម Facebook និង TikTok ក្នុងតម្លៃសមរម្យ និងឆាប់រហ័ស។\n\n"
        "👇 សូមចុចជ្រើសរើសជម្រើសខាងក្រោមដើម្បីបន្ត៖"
    )
    
    # 2. បង្កើតប៊ូតុង Reply Keyboard នៅខាងក្រោម
    keyboard = [
        ["🛍️ សេវាកម្ម", "ទំនាក់ទំនង (Contact)"],
        ["ព័ត៌មាន (About)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    if user_id in user_states:
        state = user_states[user_id]
        
        if state.get('step') == 'waiting_link':
            state['link'] = text
            state['step'] = 'waiting_slip'
            
            caption = (
                "🔗 បានទទួល Link រួចរាល់!\n\n"
                "💳 សូមធ្វើការស្កេន QR Code ខាងលើដើម្បីទូទាត់ប្រាក់ ៖\n\n"
                "📸 បន្ទាប់ពីបង់ប្រាក់រួច សូម **ផ្ញើរូបភាពវិក្កយបត្រ (Slip)** មកកាន់ឆាតនេះដើម្បីបញ្ជាក់!"
            )
            try:
                with open("qr.jpg", "rb") as qr_photo:
                    await context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=qr_photo,
                        caption=caption,
                        parse_mode="Markdown"
                    )
            except Exception as e:
                await update.message.reply_text("🔗 បានទទួល Link រួចរាល់! សូមផ្ញើ Slip មកដើម្បីបន្ត។")
                print(f"Error opening qr.jpg: {e}")
            return

    if text == "🛍️ សេវាកម្ម":
        inline_keyboard = [
            [InlineKeyboardButton("Facebook", callback_data="menu_facebook")],
            [InlineKeyboardButton("TikTok", callback_data="menu_tiktok")]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await update.message.reply_text("សូមជ្រើសរើសប្រភេទសេវាកម្មខាងក្រោម៖", reply_markup=reply_markup)
        
    elif text == "ទំនាក់ទំនង (Contact)":
        await update.message.reply_text("📞 ព័ត៌មានទំនាក់ទំនង:\n- Telegram Admin: @YourUsername\n- Channel: @YourChannel")
        
    elif text == "ព័ត៌មាន (About)":
        await update.message.reply_text("ℹ️ នេះគឺជាប្រព័ន្ធ Bot ស្វ័យប្រវត្តិសម្រាប់ជួយសម្រួលដល់ការកុម្ម៉ង់សេវាកម្ម Social Media របស់អ្នក។")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id in user_states and user_states[user_id].get('step') == 'waiting_slip':
        state = user_states[user_id]
        package = state.get('package')
        link = state.get('link')
        
        photo_file_id = update.message.photo[-1].file_id
        
        await update.message.reply_text("✅ អរគុណ! ការកុម្ម៉ង់ និងវិក្កយបត្ររបស់អ្នកត្រូវបានបញ្ជូនជូន Admin រួចរាល់ហើយ សូមរង់ចាំដំណើរការបន្ត។")
        
        GROUP_CHAT_ID = "-1003950979639"
        user = update.effective_user
        caption = (
            "🔔 **មានការបញ្ជាទិញថ្មី និងវិក្កយបត្របង់ប្រាក់!**\n\n"
            f"• សេវាកម្ម: {package}\n"
            f"• តំណរ (Link): {link}\n"
            f"• អតិថិជន: {user.first_name} (@{user.username if user.username else 'គ្មាន'})\n"
            f"• User ID: {user.id}"
        )
        try:
            await context.bot.send_photo(chat_id=GROUP_CHAT_ID, photo=photo_file_id, caption=caption, parse_mode="Markdown")
        except Exception as e:
            print(f"Error sending photo notification: {e}")
            
        del user_states[user_id]
    else:
        await update.message.reply_text("សូមជ្រើសរើសសេវាកម្មតាមរយៈមឺនុយជាមុនសិន។")

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
            [InlineKeyboardButton("1K ~ 0.70$", callback_data="buy_1k")],
            [InlineKeyboardButton("5K ~ 3.50$", callback_data="buy_5k")],
            [InlineKeyboardButton("10K ~ 7.00$", callback_data="buy_10k")],
            [InlineKeyboardButton("15K ~ 10.50$", callback_data="buy_15k")],
            [InlineKeyboardButton("20K ~ 14.00$", callback_data="buy_20k")],
            [InlineKeyboardButton("30K ~ 21.00$", callback_data="buy_30k")],
            [InlineKeyboardButton("40K ~ 28.00$", callback_data="buy_40k")],
            [InlineKeyboardButton("50K ~ 35.00$", callback_data="buy_50k")]
        ]
        reply_markup = InlineKeyboardMarkup(price_keyboard)
        await query.message.edit_text("📌 សូមជ្រើសរើសកញ្ចប់ FACEBOOK FOLLOW ៖", reply_markup=reply_markup)
        
    elif query.data == "fb_like":
        await query.message.edit_text("អ្នកបានជ្រើសរើស៖ FACEBOOK LIKE")
    elif query.data == "fb_views":
        await query.message.edit_text("អ្នកបានជ្រើសរើស៖ FACEBOOK VIEWS")
        
    elif query.data in ["buy_1k", "buy_5k", "buy_10k", "buy_15k", "buy_20k", "buy_30k", "buy_40k", "buy_50k"]:
        package_name = query.data.replace("buy_", "").upper()
        
        user_states[user_id] = {
            'step': 'waiting_link',
            'package': f"FACEBOOK FOLLOW ({package_name})"
        }
        
        await query.message.edit_text(f"អ្នកបានជ្រើសរើសកញ្ចប់ **{package_name}** ហើយ។\n\n🔗 សូមផ្ញើតំណរ (Link) ហ្វេសប៊ុករបស់អ្នកមកទីនេះ:")

if __name__ == "__main__":
    TOKEN = "8675478122:AAFem3pCVLz_zZBebYuRmWcKGFAR1FBGY5Y"
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    print("Bot កំពុងដំណើរការ...")
    app.run_polling()
