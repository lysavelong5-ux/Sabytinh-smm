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

# 2. កូដគ្រប់គ្រងរាល់សារ និងប៊ូតុងនៅខាងក្រោម
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
        
        qr_url = "https://cdn.phototourl.com/free/2026-09-01-1a3cfec5-d60d-4038-b50c-ac83f71acab2.jpg"
        caption = (
            "🔗 បានទទួល Link រួចរាល់!\n\n"
            "💳 សូមធ្វើការស្កេន QR Code ខាងលើដើម្បីទូទាត់ប្រាក់ ៖\n\n"
            "📸 បន្ទាប់ពីបង់ប្រាក់រួច សូម **ផ្ញើរូបភាពវិក្កយបត្រ (Slip)** មកកាន់ឆាតនេះដើម្បីបញ្ជាក់!"
        )
        
        try:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=qr_url,
                caption=caption,
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
            return
        except Exception as e:
            print(f"Error sending QR image: {e}")
            await update.message.reply_text(
                f"{caption}\n\n(⚠️ រូបភាព QR Code មានបញ្ហាបន្តិច ប៉ុន្តែអាចបន្តផ្ញើ Slip បាន)",
                reply_markup=reply_markup
            )
        return

    # ការជ្រើសរើសកញ្ចប់តម្លៃ Facebook Follow
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
        await update.message.reply_text(f"អ្នកបានជ្រើសរើសកញ្ចប់ **FACEBOOK FOLLOW ({package_name})** ហើយ។\n\n🔗 សូមផ្ញើតំណរ (Link) ហ្វេសប៊ុករបស់អ្នកមកទីនេះ:", reply_markup=reply_markup)
        return

    # ការជ្រើសរើសកញ្ចប់តម្លៃ Facebook Like
    if text in [
        "1K ~ 0.80$", "5K ~ 4.00$", "10K ~ 8.00$", "20K ~ 16.00$", 
        "30K ~ 24.00$", "40K ~ 32.00$", "50K ~ 40.00$", "60K ~ 48.00$", 
        "70K ~ 56.00$", "80K ~ 64.00$", "90K ~ 72.00$"
    ]:
        package_name = text.split(" ~ ")[0]
        user_states[user_id] = {
            'step': 'waiting_link',
            'package': f"FACEBOOK LIKE ({package_name})"
        }
        keyboard = [
            ["🛍️ សេវាកម្ម", "ទំនាក់ទំនង (Contact)"],
            ["ព័ត៌មាន (About)"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(f"អ្នកបានជ្រើសរើសកញ្ចប់ **FACEBOOK LIKE ({package_name})** ហើយ។\n\n🔗 សូមផ្ញើតំណរ (Link) ហ្វេសប៊ុករបស់អ្នកមកទីនេះ:", reply_markup=reply_markup)
        return

    # ការជ្រើសរើសកញ្ចប់តម្លៃ Facebook Views
    if text in [
        "1K ~ 0.53$", "5K ~ 2.65$", "10K ~ 5.30$", "20K ~ 10.60$", 
        "30K ~ 15.90$", "40K ~ 21.20$", "50K ~ 26.50$", "60K ~ 31.80$", 
        "70K ~ 37.10$", "80K ~ 42.40$", "90K ~ 47.70$", "100K ~ 53.00$"
    ]:
        package_name = text.split(" ~ ")[0]
        user_states[user_id] = {
            'step': 'waiting_link',
            'package': f"FACEBOOK VIEWS ({package_name})"
        }
        keyboard = [
            ["🛍️ សេវាកម្ម", "ទំនាក់ទំនង (Contact)"],
            ["ព័ត៌មាន (About)"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(f"អ្នកបានជ្រើសរើសកញ្ចប់ **FACEBOOK VIEWS ({package_name})** ហើយ។\n\n🔗 សូមផ្ញើតំណរ (Link) ហ្វេសប៊ុករបស់អ្នកមកទីនេះ:", reply_markup=reply_markup)
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

    elif text == "👍 Facebook Like":
        price_keyboard = [
            ["1K ~ 0.80$", "5K ~ 4.00$"],
            ["10K ~ 8.00$", "20K ~ 16.00$"],
            ["30K ~ 24.00$", "40K ~ 32.00$"],
            ["50K ~ 40.00$", "60K ~ 48.00$"],
            ["70K ~ 56.00$", "80K ~ 64.00$"],
            ["90K ~ 72.00$"],
            ["🔙 ត្រឡប់ក្រោយ"]
        ]
        reply_markup = ReplyKeyboardMarkup(price_keyboard, resize_keyboard=True)
        await update.message.reply_text("📌 សូមជ្រើសរើសកញ្ចប់ FACEBOOK LIKE ៖", reply_markup=reply_markup)

    elif text == "👁️ Facebook Views":
        price_keyboard = [
            ["1K ~ 0.53$", "5K ~ 2.65$"],
            ["10K ~ 5.30$", "20K ~ 10.60$"],
            ["30K ~ 15.90$", "40K ~ 21.20$"],
            ["50K ~ 26.50$", "60K ~ 31.80$"],
            ["70K ~ 37.10$", "80K ~ 42.40$"],
            ["90K ~ 47.70$", "100K ~ 53.00$"],
            ["🔙 ត្រឡប់ក្រោយ"]
        ]
        reply_markup = ReplyKeyboardMarkup(price_keyboard, resize_keyboard=True)
        await update.message.reply_text("📌 សូមជ្រើសរើសកញ្ចប់ FACEBOOK VIEWS ៖", reply_markup=reply_markup)

    elif text == "🎵 TikTok":
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

# 3. កូដទទួលយករូបភាព Slip ពីអតិថិជន និងបាញ់ចូល Group ព្រមទាំងភ្ជាប់ User ID ក្នុងប៊ូតុង Admin
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id in user_states and user_states[user_id].get('step') == 'waiting_slip':
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
        
        admin_keyboard = [
            [
                InlineKeyboardButton("✅ បញ្ជាក់", callback_data=f"approve_{user_id}"),
                InlineKeyboardButton("❌ មិនយល់ព្រម", callback_data=f"reject_{user_id}")
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

# 4. កូដពេល Admin ចុចប៊ូតុង ព្រមទាំងផ្ញើសារជូនដំណឹងទៅ User វិញស្វ័យប្រវត្តិ
async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    original_caption = query.message.caption or ""
    
    action, target_user_id = data.split("_")
    target_user_id = int(target_user_id)
    
    if action == "approve":
        new_caption = original_caption + "\n\n🟢 **ស្ថានភាព៖ បានបញ្ជាក់ (Approved) ✅**"
        await query.edit_message_caption(caption=new_caption, parse_mode="Markdown")
        
        try:
            await context.bot.send_message(
                chat_id=target_user_id,
                text="🎉 **ដំណឹងល្អ!** ការកុម្ម៉ង់សេវាកម្មរបស់អ្នកត្រូវបាន Admin **បញ្ជាក់ (Approved) ✅** រួចរាល់ហើយ! យើងកំពុងដំណើរការជូនលោកអ្នកឆាប់ៗនេះ។",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Error notifying user: {e}")
            
    elif action == "reject":
        new_caption = original_caption + "\n\n🔴 **ស្ថានភាព៖ មិនយល់ព្រម / បដិសេធ (Rejected) ❌**"
        await query.edit_message_caption(caption=new_caption, parse_mode="Markdown")
        
        try:
            await context.bot.send_message(
                chat_id=target_user_id,
                text="❌ **សូមអភ័យទោស!** ការកុម្ម៉ង់សេវាកម្មរបស់អ្នកត្រូវបាន Admin **មិនយល់ព្រម (Rejected) ❌** (អាចមកពីវិក្កយបត្រមិនត្រឹមត្រូវ)។ សូមទំនាក់ទំនងមកកាន់ Admin ផ្ទាល់។",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Error notifying user: {e}")

if __name__ == "__main__":
    TOKEN = "8675478122:AAFem3pCVLz_zZBebYuRmWcKGFAR1FBGY5Y"
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(CallbackQueryHandler(admin_callback))
    
    print("Bot កំពុងដំណើរការ...")
    app.run_polling()
