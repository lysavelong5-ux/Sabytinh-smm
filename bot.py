import os
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

user_states = {}
user_balances = {}
user_languages = {}

ADMIN_USERNAME = "@NEAKKROBKRONG"

TEXTS = {
    "khmer": {
        "welcome": "🙏 សួស្តីស្វាគមន៍មកកាន់ប្រព័ន្ធសេវាកម្ម Social Media របស់យើង!\n\n👇 សូមជ្រើសរើសជម្រើសខាងក្រោម៖",
        "services": "🛍️ សេវាកម្ម",
        "account": "🪪 គណនី",
        "add_fund": "💸 Add Fund",
        "lang": "🌐 ភាសា",
        "contact": "📞 ទំនាក់ទំនង",
        "about": "ℹ️ ព័ត៌មាន",
        "back": "🔙 ត្រឡប់ក្រោយ",
        "platform_select": "📌 សូមជ្រើសរើសប្រភេទ Platform ៖",
        "fb_select": "📌 សូមជ្រើសរើសសេវាកម្ម Facebook ៖",
        "link_prompt": "🔗 បានទទួលតំណរ (Link) រួចរាល់!\n\n✅ ឥឡូវនេះការកុម្ម៉ង់របស់អ្នកត្រូវបានបញ្ជូនជូន Admin រួចរាល់ហើយ។ សូមរង់ចាំការពិនិត្យបន្តិច!",
        "add_fund_prompt": "💸 **បន្ថែមទឹកប្រាក់ (Add Fund)**\n\nសូមវាយបញ្ចូលចំនួនទឹកប្រាក់ដែលអ្នកចង់បន្ថែម (ឧទាហរណ៍: `10` ឬ `5.5` ជាលុយដុល្លារ):",
        "slip_prompt": "📸 សូមផ្ញើរូបភាពវិក្កយបត្រ (Slip) នៃការបង់ប្រាក់របស់អ្នកមកទីនេះ ដើម្បីឱ្យ Admin ពិនិត្យ និងបញ្ជាក់!",
        "account_info": "🪪 **ព័ត៌មានគណនីរបស់អ្នក**\n\n• Username: {username}\n• ID: {user_id}\n• Balance: ${balance:.2f}",
        "contact_info": f"📞 ព័ត៌មានទំនាក់ទំនង Admin:\n- Telegram: {ADMIN_USERNAME}",
        "about_info": "ℹ️ នេះគឺជាប្រព័ន្ធស្វ័យប្រវត្តិសម្រាប់បញ្ជាទិញសេវាកម្ម Social Media ក្នុងតម្លៃសមរម្យ។",
        "lang_select": "🌐 សូមជ្រើសរើសភាសាដែលលោកអ្នកចង់ប្រើប្រាស់៖"
    },
    "english": {
        "welcome": "👋 Welcome to our Social Media service system!\n\n👇 Please select an option below:",
        "services": "🛍️ Services",
        "account": "🪪 Account",
        "add_fund": "💸 Add Fund",
        "lang": "🌐 Language",
        "contact": "📞 Contact",
        "about": "ℹ️ About",
        "back": "🔙 Back",
        "platform_select": "📌 Please select a Platform:",
        "fb_select": "📌 Please select Facebook service:",
        "link_prompt": "🔗 Link received successfully!\n\n✅ Your order has been sent to Admin. Please wait for processing!",
        "add_fund_prompt": "💸 **Add Fund**\n\nPlease enter the amount you want to top up (e.g. `10` or `5.5` in USD):",
        "slip_prompt": "📸 Please send your payment Slip here for Admin review and approval!",
        "account_info": "🪪 **Your Account Information**\n\n• Username: {username}\n• ID: {user_id}\n• Balance: ${balance:.2f}",
        "contact_info": f"📞 Contact Admin:\n- Telegram: {ADMIN_USERNAME}",
        "about_info": "ℹ️ This is an automated bot for Social Media services.",
        "lang_select": "🌐 Please select your preferred language:"
    }
}

def get_lang(user_id):
    return user_languages.get(user_id, "khmer")

def get_main_keyboard(lang):
    t = TEXTS[lang]
    return ReplyKeyboardMarkup([
        [t["services"], t["account"]],
        [t["add_fund"], t["lang"]],
        [t["contact"], t["about"]]
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

    # 1. ដំណាក់កាលរង់ចាំ Link (សម្រាប់បញ្ជាទិញសេវាកម្ម)
    if user_id in user_states and user_states[user_id].get('step') == 'waiting_link':
        package = user_states[user_id].get('package')
        link = text
        
        await update.message.reply_text(t["link_prompt"], reply_markup=get_main_keyboard(lang))
        
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
            "🔔 **មានការបញ្ជាទិញសេវាកម្មថ្មី!**\n\n"
            f"• សេវាកម្ម: {package}\n"
            f"• តំណរ (Link): {link}\n"
            f"• អតិថិជន: {user.first_name} (@{user.username if user.username else 'None'})\n"
            f"• User ID: {user.id}"
        )
        try:
            await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=caption, reply_markup=admin_markup, parse_mode="Markdown")
        except Exception as e:
            print(f"Error sending order notification: {e}")
            
        del user_states[user_id]
        return

    # 2. ដំណាក់កាលរង់ចាំចំនួនទឹកប្រាក់សម្រាប់ Add Fund
    if user_id in user_states and user_states[user_id].get('step') == 'waiting_fund_amount':
        try:
            amount = float(text)
            if amount <= 0:
                raise ValueError()
            
            user_states[user_id] = {'step': 'waiting_fund_slip', 'amount': amount}
            await update.message.reply_text(f"✅ Amount: ${amount:.2f}\n\n{t['slip_prompt']}", reply_markup=get_main_keyboard(lang))
        except ValueError:
            await update.message.reply_text("❌ សូមបញ្ចូលជាតួលេខឱ្យបានត្រឹមត្រូវ (ឧទាហរណ៍: 10 ឬ 5.5):")
        return

    # ការជ្រើសរើសកញ្ចប់តម្លៃ Facebook Follow
    if text in ["1K ~ 0.70$", "5K ~ 3.50$", "10K ~ 7.00$", "15K ~ 10.50$", "20K ~ 14.00$", "30K ~ 21.00$", "40K ~ 28.00$", "50K ~ 35.00$"]:
        package_name = text.split(" ~ ")[0]
        user_states[user_id] = {'step': 'waiting_link', 'package': f"FACEBOOK FOLLOW ({package_name})"}
        await update.message.reply_text(f"Selected: FACEBOOK FOLLOW ({package_name})\n\n🔗 សូមផ្ញើតំណរ (Link) របស់អ្នកមកទីនេះ៖", reply_markup=get_main_keyboard(lang))
        return

    # ការជ្រើសរើសកញ្ចប់តម្លៃ Facebook Like
    if text in ["1K ~ 0.80$", "5K ~ 4.00$", "10K ~ 8.00$", "20K ~ 16.00$", "30K ~ 24.00$", "40K ~ 32.00$", "50K ~ 40.00$", "60K ~ 48.00$", "70K ~ 56.00$", "80K ~ 64.00$", "90K ~ 72.00$"]:
        package_name = text.split(" ~ ")[0]
        user_states[user_id] = {'step': 'waiting_link', 'package': f"FACEBOOK LIKE ({package_name})"}
        await update.message.reply_text(f"Selected: FACEBOOK LIKE ({package_name})\n\n🔗 សូមផ្ញើតំណរ (Link) របស់អ្នកមកទីនេះ៖", reply_markup=get_main_keyboard(lang))
        return

    # ការជ្រើសរើសកញ្ចប់តម្លៃ Facebook Views
    if text in ["1K ~ 0.53$", "5K ~ 2.65$", "10K ~ 5.30$", "20K ~ 10.60$", "30K ~ 15.90$", "40K ~ 21.20$", "50K ~ 26.50$", "60K ~ 31.80$", "70K ~ 37.10$", "80K ~ 42.40$", "90K ~ 47.70$", "100K ~ 53.00$"]:
        package_name = text.split(" ~ ")[0]
        user_states[user_id] = {'step': 'waiting_link', 'package': f"FACEBOOK VIEWS ({package_name})"}
        await update.message.reply_text(f"Selected: FACEBOOK VIEWS ({package_name})\n\n🔗 សូមផ្ញើតំណរ (Link) របស់អ្នកមកទីនេះ៖", reply_markup=get_main_keyboard(lang))
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

    elif text == t["add_fund"]:
        user_states[user_id] = {'step': 'waiting_fund_amount'}
        await update.message.reply_text(t["add_fund_prompt"], reply_markup=get_main_keyboard(lang), parse_mode="Markdown")

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
        await update.message.reply_text(t["contact_info"], parse_mode="Markdown")
        
    elif text == t["about"]:
        await update.message.reply_text(t["about_info"])

# 3. មុខងារទទួលរូបភាព (Slip សម្រាប់ Add Fund)
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    t = TEXTS[lang]
    
    if user_id in user_states and user_states[user_id].get('step') == 'waiting_fund_slip':
        state = user_states[user_id]
        amount = state.get('amount')
        
        photo_file_id = update.message.photo[-1].file_id
        await update.message.reply_text("✅ អរគុណ! វិក្កយបត្រដាក់ប្រាក់របស់អ្នកត្រូវបានបញ្ជូនជូន Admin រួចរាល់ហើយ។ សូមរង់ចាំការផ្ទៀងផ្ទាត់!", reply_markup=get_main_keyboard(lang))
        
        admin_keyboard = [
            [
                InlineKeyboardButton("Approve Fund", callback_data=f"fundapprove_{user_id}_{amount}"),
                InlineKeyboardButton("Reject", callback_data=f"fundreject_{user_id}")
            ]
        ]
        admin_markup = InlineKeyboardMarkup(admin_keyboard)
        
        GROUP_CHAT_ID = "-1003950979639"
        user = update.effective_user
        caption = (
            "💸 **មានសំណើដាក់ប្រាក់ (Add Fund) ថ្មី!**\n\n"
            f"• ចំនួនទឹកប្រាក់: ${amount:.2f}\n"
            f"• អតិថិជន: {user.first_name} (@{user.username if user.username else 'None'})\n"
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
            print(f"Error sending fund photo: {e}")
            
        del user_states[user_id]
    else:
        await update.message.reply_text("សូមជ្រើសរើសមុខងារ Add Fund ជាមុនសិន។")

# 4. មុខងារ Admin ចុច Approve ឬ Reject
async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    original_caption = query.message.caption or ""
    
    parts = data.split("_")
    action = parts[0]
    target_user_id = int(parts[1])
    
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
        
    elif action == "fundapprove":
        amount = float(parts[2])
        # បន្ថែមទឹកប្រាក់ចូល Balance របស់ User ស្វ័យប្រវត្តិ
        if target_user_id not in user_balances:
            user_balances[target_user_id] = 0.00
        user_balances[target_user_id] += amount
        
        new_balance = user_balances[target_user_id]
        await query.edit_message_caption(caption=original_caption + f"\n\nStatus: Approved ✅ (+${amount:.2f})", parse_mode="Markdown")
        try:
            await context.bot.send_message(
                chat_id=target_user_id, 
                text=f"🎉 **ដំណឹងល្អ!** Admin បានបញ្ជាក់ការដាក់ប្រាក់របស់អ្នកចំនួន **${amount:.2f}** រួចរាល់ហើយ!\n💰 សមតុល្យបច្ចុប្បន្ន (Balance): **${new_balance:.2f}**",
                parse_mode="Markdown"
            )
        except: pass
        
    elif action == "fundreject":
        await query.edit_message_caption(caption=original_caption + "\n\nStatus: Rejected ❌", parse_mode="Markdown")
        try:
            await context.bot.send_message(chat_id=target_user_id, text="❌ សំណើដាក់ប្រាក់របស់អ្នកត្រូវបាន Admin បដិសេធ (Rejected)។ សូមទាក់ទងមកកាន់ Admin។")
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
