import os
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

user_states = {}
user_balances = {}
user_languages = {}  # សម្រាប់រក្សាទុកភាសាដែលអតិថិជនបានជ្រើសរើស (khmer ឬ english)

# អត្ថបទសម្រាប់បង្ហាញតាមភាសាផ្សេងៗ
TEXTS = {
    "khmer": {
        "welcome": "🙏 សួស្តីស្វាគមន៍មកកាន់ប្រព័ន្ធសេវាកម្ម Social Media របស់យើង!\n\n👇 សូមជ្រើសរើសជម្រើសខាងក្រោម៖",
        "services": "🛍️ សេវាកម្ម",
        "account": "🪪 គណនី",
        "lang": "🌐 ភាសា",
        "contact": "📞 ទំនាក់ទំនង",
        "about": "ℹ️ ព័ត៌មាន",
        "back": "🔙 ត្រឡប់ក្រោយ",
        "platform_select": "📌 សូមជ្រើសរើសប្រភេទ Platform ៖",
        "fb_select": "📌 សូមជ្រើសរើសសេវាកម្ម Facebook ៖",
        "link_prompt": "🔗 បានទទួលកញ្ចប់សេវាកម្មរួចរាល់!\n\n🔗 សូមផ្ញើតំណរ (Link) របស់អ្នកមកទីនេះ៖",
        "qr_prompt": "💳 សូមធ្វើការស្កេន QR Code ខាងលើដើម្បីទូទាត់ប្រាក់ ៖\n\n📸 បន្ទាប់ពីបង់ប្រាក់រួច សូម **ផ្ញើរូបភាពវិក្កយបត្រ (Slip)** មកកាន់ឆាតនេះដើម្បីបញ្ជាក់!",
        "success_slip": "✅ អរគុណ! ការកុម្ម៉ង់ និងវិក្កយបត្ររបស់អ្នកត្រូវបានបញ្ជូនជូន Admin រួចរាល់ហើយ។",
        "account_info": "🪪 **ព័ត៌មានគណនីរបស់អ្នក**\n\n• Username: {username}\n• ID: {user_id}\n• Balance: ${balance:.2f}",
        "contact_info": "📞 ព័ត៌មានទំនាក់ទំនង Admin:\n- Telegram: @YourUsername",
        "about_info": "ℹ️ នេះគឺជាប្រព័ន្ធស្វ័យប្រវត្តិសម្រាប់បញ្ជាទិញសេវាកម្ម Social Media ក្នុងតម្លៃសមរម្យ។",
        "lang_select": "🌐 សូមជ្រើសរើសភាសាដែលលោកអ្នកចង់ប្រើប្រាស់៖"
    },
    "english": {
        "welcome": "👋 Welcome to our Social Media service system!\n\n👇 Please select an option below:",
        "services": "🛍️ Services",
        "account": "🪪 Account",
        "lang": "🌐 Language",
        "contact": "📞 Contact",
        "about": "ℹ️ About",
        "back": "🔙 Back",
        "platform_select": "📌 Please select a Platform:",
        "fb_select": "📌 Please select Facebook service:",
        "link_prompt": "🔗 Package selected successfully!\n\n🔗 Please send your Link here:",
        "qr_prompt": "💳 Please scan the QR Code above to make payment:\n\n📸 After payment, please send your payment Slip here!",
        "success_slip": "✅ Thank you! Your order and payment slip have been sent to Admin.",
        "account_info": "🪪 **Your Account Information**\n\n• Username: {username}\n• ID: {user_id}\n• Balance: ${balance:.2f}",
        "contact_info": "📞 Contact Admin:\n- Telegram: @YourUsername",
        "about_info": "ℹ️ This is an automated bot for Social Media services.",
        "lang_select": "🌐 Please select your preferred language:"
    }
}

def get_lang(user_id):
    return user_languages.get(user_id, "khmer")  # កំណត់ភាសាខ្មែរជាលំនាំដើម

def get_main_keyboard(lang):
    t = TEXTS[lang]
    return ReplyKeyboardMarkup([
        [t["services"], t["account"]],
        [t["lang"], t["contact"]],
        [t["about"]]
    ], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    await update.message.reply_text(TEXTS[lang]["welcome"], reply_markup=get_main_keyboard(lang))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    lang = get_lang(user_id)
    t = TEXTS[lang]
    
    if user_id not in user_balances:
        user_balances[user_id] = 0.00

    # ដំណាក់កាលរង់ចាំ Link
    if user_id in user_states and user_states[user_id].get('step') == 'waiting_link':
        state = user_states[user_id]
        state['link'] = text
        state['step'] = 'waiting_slip'
        
        qr_url = "https://cdn.phototourl.com/free/2026-09-01-1a3cfec5-d60d-4038-b50c-ac83f71acab2.jpg"
        caption = f"{t['link_prompt']}\n\n{t['qr_prompt']}"
        
        try:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=qr_url,
                caption=caption,
                parse_mode="Markdown",
                reply_markup=get_main_keyboard(lang)
            )
            return
        except Exception as e:
            print(f"Error sending QR image: {e}")
            await update.message.reply_text(caption, reply_markup=get_main_keyboard(lang))
        return

    # ការជ្រើសរើសកញ្ចប់តម្លៃ
    if text in ["1K ~ 0.70$", "5K ~ 3.50$", "10K ~ 7.00$", "15K ~ 10.50$", "20K ~ 14.00$", "30K ~ 21.00$", "40K ~ 28.00$", "50K ~ 35.00$"]:
        package_name = text.split(" ~ ")[0]
        user_states[user_id] = {'step': 'waiting_link', 'package': f"FACEBOOK FOLLOW ({package_name})"}
        await update.message.reply_text(f"Selected: FACEBOOK FOLLOW ({package_name})\n\n{t['link_prompt']}", reply_markup=get_main_keyboard(lang))
        return

    if text in ["1K ~ 0.80$", "5K ~ 4.00$", "10K ~ 8.00$", "20K ~ 16.00$", "30K ~ 24.00$", "40K ~ 32.00$", "50K ~ 40.00$", "60K ~ 48.00$", "70K ~ 56.00$", "80K ~ 64.00$", "90K ~ 72.00$"]:
        package_name = text.split(" ~ ")[0]
        user_states[user_id] = {'step': 'waiting_link', 'package': f"FACEBOOK LIKE ({package_name})"}
        await update.message.reply_text(f"Selected: FACEBOOK LIKE ({package_name})\n\n{t['link_prompt']}", reply_markup=get_main_keyboard(lang))
        return

    if text in ["1K ~ 0.53$", "5K ~ 2.65$", "10K ~ 5.30$", "20K ~ 10.60$", "30K ~ 15.90$", "40K ~ 21.20$", "50K ~ 26.50$", "60K ~ 31.80$", "70K ~ 37.10$", "80K ~ 42.40$", "90K ~ 47.70$", "100K ~ 53.00$"]:
        package_name = text.split(" ~ ")[0]
        user_states[user_id] = {'step': 'waiting_link', 'package': f"FACEBOOK VIEWS ({package_name})"}
        await update.message.reply_text(f"Selected: FACEBOOK VIEWS ({package_name})\n\n{t['link_prompt']}", reply_markup=get_main_keyboard(lang))
        return

    # ការរុករកម៉ឺនុយ
    if text == t["services"]:
        keyboard = [
            ["📘 Facebook", "🎵 TikTok"],
            [t["back"]]
        ]
        await update.message.reply_text(t["platform_select"], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        
    elif text == t["account"]:
        user = update.effective_user
        username = f"@{user.username}" if user.username else "No Username"
        balance = user_balances.get(user_id, 0.00)
        account_msg = t["account_info"].format(username=username, user_id=user.id, balance=balance)
        await update.message.reply_text(account_msg, reply_markup=get_main_keyboard(lang), parse_mode="Markdown")

    elif text == t["lang"]:
        lang_keyboard = [
            ["🇰🇭 ភាសាខ្មែរ", "🇬🇧 English"],
            [t["back"]]
        ]
        await update.message.reply_text(t["lang_select"], reply_markup=ReplyKeyboardMarkup(lang_keyboard, resize_keyboard=True))

    elif text in ["🇰🇭 ភាសាខ្មែរ", "🇰🇭 Khmer"]:
        user_languages[user_id] = "khmer"
        await update.message.reply_text("✅ បានប្តូរទៅជាភាសាខ្មែរជោគជ័យ!", reply_markup=get_main_keyboard("khmer"))

    elif text in ["🇬🇧 English"]:
        user_languages[user_id] = "english"
        await update.message.reply_text("✅ Switched to English successfully!", reply_markup=get_main_keyboard("english"))

    elif text == "📘 Facebook":
        keyboard = [
            ["👥 Facebook Follow", "👍 Facebook Like"],
            ["👁️ Facebook Views", t["back"]]
        ]
        await update.message.reply_text(t["fb_select"], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        
    elif text == "👥 Facebook Follow":
        price_keyboard = [
            ["1K ~ 0.70$", "5K ~ 3.50$"],
            ["10K ~ 7.00$", "15K ~ 10.50$"],
            ["20K ~ 14.00$", "30K ~ 21.00$"],
            ["40K ~ 28.00$", "50K ~ 35.00$"],
            [t["back"]]
        ]
        await update.message.reply_text("FACEBOOK FOLLOW:", reply_markup=ReplyKeyboardMarkup(price_keyboard, resize_keyboard=True))

    elif text == "👍 Facebook Like":
        price_keyboard = [
            ["1K ~ 0.80$", "5K ~ 4.00$"],
            ["10K ~ 8.00$", "20K ~ 16.00$"],
            ["30K ~ 24.00$", "40K ~ 32.00$"],
            ["50K ~ 40.00$", "60K ~ 48.00$"],
            ["70K ~ 56.00$", "80K ~ 64.00$"],
            ["90K ~ 72.00$"],
            [t["back"]]
        ]
        await update.message.reply_text("FACEBOOK LIKE:", reply_markup=ReplyKeyboardMarkup(price_keyboard, resize_keyboard=True))

    elif text == "👁️ Facebook Views":
        price_keyboard = [
            ["1K ~ 0.53$", "5K ~ 2.65$"],
            ["10K ~ 5.30$", "20K ~ 10.60$"],
            ["30K ~ 15.90$", "40K ~ 21.20$"],
            ["50K ~ 26.50$", "60K ~ 31.80$"],
            ["70K ~ 37.10$", "80K ~ 42.40$"],
            ["90K ~ 47.70$", "100K ~ 53.00$"],
            [t["back"]]
        ]
        await update.message.reply_text("FACEBOOK VIEWS:", reply_markup=ReplyKeyboardMarkup(price_keyboard, resize_keyboard=True))

    elif text == "🎵 TikTok":
        await update.message.reply_text("TikTok service coming soon!")

    elif text == t["back"]:
        await update.message.reply_text(t["welcome"], reply_markup=get_main_keyboard(lang))
        
    elif text == t["contact"]:
        await update.message.reply_text(t["contact_info"])
        
    elif text == t["about"]:
        await update.message.reply_text(t["about_info"])

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    t = TEXTS[lang]
    
    if user_id in user_states and user_states[user_id].get('step') == 'waiting_slip':
        state = user_states[user_id]
        package = state.get('package')
        link = state.get('link')
        
        photo_file_id = update.message.photo[-1].file_id
        await update.message.reply_text(t["success_slip"], reply_markup=get_main_keyboard(lang))
        
        admin_keyboard = [
            [
                InlineKeyboardButton("Approve", callback_data=f"approve_{user_id}"),
                InlineKeyboardButton("Reject", callback_data=f"reject_{user_id}")
            ]
        ]
        admin_markup = InlineKeyboardMarkup(admin_keyboard)
        
        GROUP_CHAT_ID = "-1003950979639"
        user = update.effective_user
        caption = (
            "New Order & Payment Slip!\n\n"
            f"• Service: {package}\n"
            f"• Link: {link}\n"
            f"• Customer: {user.first_name} (@{user.username if user.username else 'None'})\n"
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
            print(f"Error sending photo: {e}")
            
        del user_states[user_id]
    else:
        await update.message.reply_text("Please select a service first.")

async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    original_caption = query.message.caption or ""
    action, target_user_id = data.split("_")
    target_user_id = int(target_user_id)
    
    if action == "approve":
        await query.edit_message_caption(caption=original_caption + "\n\nStatus: Approved ✅", parse_mode="Markdown")
        try:
            await context.bot.send_message(chat_id=target_user_id, text="Your order has been Approved! ✅")
        except: pass
    elif action == "reject":
        await query.edit_message_caption(caption=original_caption + "\n\nStatus: Rejected ❌", parse_mode="Markdown")
        try:
            await context.bot.send_message(chat_id=target_user_id, text="Your order has been Rejected. ❌")
        except: pass

if __name__ == "__main__":
    TOKEN = "8675478122:AAFem3pCVLz_zZBebYuRmWcKGFAR1FBGY5Y"
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(CallbackQueryHandler(admin_callback))
    
    print("Bot is running...")
    app.run_polling()
