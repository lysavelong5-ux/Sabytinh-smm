from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

user_states = {}

# 1. កូដពេលចាប់ផ្តើម /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 សួស្តីស្វាគមន៍មកកាន់ប្រព័ន្ធបំរើសេវាកម្ម Social Media របស់យើង!\n\n"
        "✨ ទីនេះមានទទួលកុម្ម៉ង់សេវាកម្ម Facebook និង TikTok ក្នុងតម្លៃសមរម្យ និងឆាប់រហ័ស។\n\n"
        "👇 សូមចុចជ្រើសរើសជម្រើសខាងក្រោម៖"
    )
    keyboard = [
        ["🛍️ សេវាកម្ម", "ទំនាក់ទំនង (Contact)"],
        ["ព័ត៌មាន (About)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# 2. កូដគ្រប់គ្រងរាល់ការចុចលើ Reply Keyboard
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    # ដំណាក់កាលរង់ចាំ Link
    if user_id in user_states and user_states[user_id].get('step') == 'waiting_link':
        state = user_states[user_id]
        state['link'] = text
        state['step'] = 'waiting_slip'
        
        keyboard = [
            ["🛍️ សេវាកម្ម", "ទំនាក់ទំនង (Contact)"],
            ["ព័ត៌មាន (About)"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
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
            await update.message.reply_text("🔗 បានទទួល Link រួចរាល់! សូមផ្ញើ Slip មកដើម្បីបន្ត។", reply_markup=reply_markup)
            print(f"Error opening qr.jpg: {e}")
        return

    # ការជ្រើសរើសកញ្ចប់តម្លៃពីតារាងខាងក្រោម
    if text in ["1K ~ 0.70$", "5K ~ 3.50$", "10K ~ 7.00$", "15K ~ 10.50$", "20K ~ 14.00$", "30K ~ 21.00$", "40K ~ 28.00$", "50K ~ 35.00$"]:
        package_name = text.split(" ~ ")[0]
        
        user_states[user_id] = {
            'step': 'waiting_link',
            'package': f"FACEBOOK FOLLOW ({package_name})"
        }
        
        keyboard = [
            ["🛍️ សេវាកម្ម", "ទំនាក់ទំនង (Contact)"],
            ["ព័ត៌មាន (About)"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(f"អ្នកបានជ្រើសរើសកញ្ចប់ **{package_name}** ហើយ។\n\n🔗 សូមផ្ញើតំណរ (Link) ហ្វេសប៊ុករបស់អ្នកមកទីនេះ:", reply_markup=reply_markup)
        return

    # ម៉ឺនុយមេ
    if text == "🛍️ សេវាកម្ម":
        keyboard = [
            ["📘 Facebook", "🎵 TikTok"],
            ["🔙 ត្រឡប់ក្រោយ"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("📌 សូមជ្រើសរើសប្រភេទ Platform ៖", reply_markup=reply_markup)
        
    elif text == "📘 Facebook":
        keyboard = [
            ["👥 Facebook Follow", "👍 Facebook Like"],
            ["👁️ Facebook Views", "🔙 ត្រឡប់ក្រោយ"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("📌 សូមជ្រើសរើសសេវាកម្ម Facebook ៖", reply_markup=reply_markup)
        
    elif text == "👥 Facebook Follow":
        price_keyboard = [
            ["1K ~ 0.70$", "5K ~ 3.50$"],
            ["10K ~ 7.00$", "15K ~ 10.50$"],
            ["20K ~ 14.00$", "30K ~ 21.00$"],
            ["40K ~ 28.00$", "50K ~ 35.00$"],
            ["🔙 ត្រឡប់ក្រោយ"]
        ]
        reply_markup = ReplyKeyboardMarkup(price_keyboard, resize_keyboard=True)
        await update.message.reply_text("📌 សូមជ្រើសរើសកញ្ចប់ FACEBOOK FOLLOW ៖", reply_markup=reply_markup)

    elif text in ["👍 Facebook Like", "👁️ Facebook Views", "🎵 TikTok"]:
        await update.message.reply_text("🛠️ សេវាកម្មនេះកំពុងរៀបចំឡើង សូមអភ័យទោសចំពោះភាពអាក់ខាន!")

    elif text == "🔙 ត្រឡប់ក្រោយ":
        keyboard = [
            ["🛍️ សេវាកម្ម", "ទំនាក់ទំនង (Contact)"],
            ["ព័ត៌មាន (About)"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("សូមជ្រើសរើសជម្រើសខាងក្រោម៖", reply_markup=reply_markup)
        
    elif text == "ទំនាក់ទំនង (Contact)":
        await update.message.reply_text("📞 ព័ត៌មានទំនាក់ទំនង:\n- Telegram Admin: @YourUsername")
        
    elif text == "ព័ត៌មាន (About)":
        await update.message.reply_text("ℹ️ នេះគឺជាប្រព័ន្ធ Bot ស្វ័យប្រវត្តិសម្រាប់សេវាកម្ម Social Media។")

# 3. កូដទទួលយករូបភាព Slip ពីអតិថិជន និងបាញ់ចូល Group ព្រមទាំងដាក់ប៊ូតុង Admin
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id in user_states and user_states[user_id].get('step'] == 'waiting_slip':
        state = user_states[user_id]
        package = state.get('package')
        link = state.get('link')
        
        photo_file_id = update.message.photo[-1].file_id
        
        keyboard = [
            ["🛍️ សេវាកម្ម", "ទំនាក់ទំនង (Contact)"],
            ["ព័ត៌មាន (About)"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text("✅ អរគុណ! ការកុម្ម៉ង់ និងវិក្កយបត្ររបស់អ្នកត្រូវបានបញ្ជូនជូន Admin រួចរាល់ហើយ។", reply_markup=reply_markup)
        
        # បង្កើតប៊ូតុង Inline សម្រាប់ Admin ក្នុង Group
        admin_keyboard = [
            [
                InlineKeyboardButton("✅ បញ្ជាក់", callback_data="admin_approve"),
                InlineKeyboardButton("❌ មិនយល់ព្រម", callback_data="admin_reject")
            ]
        ]
        admin_markup = InlineKeyboardMarkup(admin_keyboard)
        
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
            await context.bot.send_photo(
                chat_id=GROUP_CHAT_ID, 
                photo=photo_file_id, 
                caption=caption, 
                reply_markup=admin_markup, 
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Error sending photo notification: {e}")
            
        del user_states[user_id]
    else:
        await update.message.reply_text("សូមជ្រើសរើសសេវាកម្មតាមរយៈមឺនុយជាមុនសិន។")

# 4. កូដពេល Admin ចុចលើប៊ូតុង បញ្ជាក់ ឬ មិនយល់ព្រម ក្នុង Group
async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    original_caption = query.message.caption or ""
    
    if data == "admin_approve":
        new_caption = original_caption + "\n\n🟢 **ស្ថានភាព៖ បានបញ្ជាក់ (Approved) ✅**"
        await query.edit_message_caption(caption=new_caption, parse_mode="Markdown")
    elif data == "admin_reject":
        new_caption = original_caption + "\n\n🔴 **ស្ថានភាព៖ មិនយល់ព្រម / បដិសេធ (Rejected) ❌**"
        await query.edit_message_caption(caption=new_caption, parse_mode="Markdown")

if __name__ == "__main__":
    TOKEN = "8675478122:AAFem3pCVLz_zZBebYuRmWcKGFAR1FBGY5Y"
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(CallbackQueryHandler(admin_callback))
    
    print("Bot កំពុងដំណើរការ...")
    app.run_polling()
