import os
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

user_states = {}
user_balances = {}
user_languages = {}

ADMIN_USERNAME = "@NEAKKROBKRONG"

PRICES = {
    "FACEBOOK FOLLOW (1K)": 0.70, "FACEBOOK FOLLOW (5K)": 3.50, "FACEBOOK FOLLOW (10K)": 7.00, "FACEBOOK FOLLOW (15K)": 10.50,
    "FACEBOOK FOLLOW (20K)": 14.00, "FACEBOOK FOLLOW (30K)": 21.00, "FACEBOOK FOLLOW (40K)": 28.00, "FACEBOOK FOLLOW (50K)": 35.00,
    
    "FACEBOOK LIKE (1K)": 0.80, "FACEBOOK LIKE (5K)": 4.00, "FACEBOOK LIKE (10K)": 8.00, "FACEBOOK LIKE (20K)": 16.00,
    "FACEBOOK LIKE (30K)": 24.00, "FACEBOOK LIKE (40K)": 32.00, "FACEBOOK LIKE (50K)": 40.00, "FACEBOOK LIKE (60K)": 48.00,
    "FACEBOOK LIKE (70K)": 56.00, "FACEBOOK LIKE (80K)": 64.00, "FACEBOOK LIKE (90K)": 72.00,
    
    "FACEBOOK VIEWS (1K)": 0.53, "FACEBOOK VIEWS (5K)": 2.65, "FACEBOOK VIEWS (10K)": 5.30, "FACEBOOK VIEWS (20K)": 10.60,
    "FACEBOOK VIEWS (30K)": 15.90, "FACEBOOK VIEWS (40K)": 21.20, "FACEBOOK VIEWS (50K)": 26.50, "FACEBOOK VIEWS (60K)": 31.80,
    "FACEBOOK VIEWS (70K)": 37.10, "FACEBOOK VIEWS (80K)": 42.40, "FACEBOOK VIEWS (90K)": 47.70, "FACEBOOK VIEWS (100K)": 53.00
}

TEXTS = {
    "khmer": {
        "welcome": "🙏 សួស្តីស្វាគមន៍មកកាន់ប្រព័ន្ធសេវាកម្ម Social Media របស់យើង!\n\n👇 សូមជ្រើសរើសជម្រើសខាងក្រោម៖",
        "services": "🛍️ សេវាកម្ម", "account": "🪪 គណនី", "add_fund": "💸 Add Fund", "lang": "🌐 ភាសា",
        "contact": "📞 ទំនាក់ទំនង", "about": "ℹ️ ព័ត៌មាន", "back": "🔙 ត្រឡប់ក្រោយ",
        "platform_select": "📌 សូមជ្រើសរើសប្រភេទ Platform ៖", "fb_select": "📌 សូមជ្រើសរើសសេវាកម្ម Facebook ៖",
        "link_prompt": "🔗 បានជ្រើសរើសកញ្ចប់: **{package}** (តម្លៃ: **${price:.2f}**)\n\n🔗 សូមផ្ញើតំណរ (Link) របស់អ្នកមកទីនេះ៖",
        "insufficient_balance": "❌ **ទឹកប្រាក់ក្នុងគណនីរបស់អ្នកមិនគ្រប់គ្រាន់ទេ!**\n\n• តម្លៃសេវាកម្ម: **${price:.2f}**\n• Balance របស់អ្នក: **${balance:.2f}**\n\n👇 សូមចុចប៊ូតុង **💸 Add Fund** ដើម្បីបន្ថែមទឹកប្រាក់ជាមុនសិន!",
        "success_order": "✅ អរគុណ! ការកុម្ម៉ង់របស់អ្នកត្រូវបានកាត់លុយ និងបញ្ជូនជូន Admin រួចរាល់ហើយ។",
        "add_fund_prompt": "💸 **បន្ថែមទឹកប្រាក់ (Add Fund)**\n\nសូមវាយបញ្ចូលចំនួនទឹកប្រាក់ដែលអ្នកចង់បន្ថែម (ឧទាហរណ៍: `10` ឬ `5.5` ជាលុយដុល្លារ):",
        "slip_prompt": "📸 សូមផ្ញើរូបភាពវិក្កយបត្រ (Slip) នៃការបង់ប្រាក់របស់អ្នកមកទីនេះ ដើម្បីឱ្យ Admin ពិនិត្យ!",
        "slip_success": "✅ អរគុណ! វិក្កយបត្រដាក់ប្រាក់ត្រូវបានបញ្ជូនជូន Admin រួចរាល់ហើយ។",
        "account_info": "🪪 **ព័ត៌មានគណនីរបស់អ្នក**\n\n• Username: {username}\n• ID: {user_id}\n• Balance: ${balance:.2f}",
        "contact_info": f"📞 ព័ត៌មានទំនាក់ទំនង Admin:\n- Telegram: {ADMIN_USERNAME}",
        "about_info": "ℹ️ នេះគឺជាប្រព័ន្ធស្វ័យប្រវត្តិសម្រាប់បញ្ជាទិញសេវាកម្ម Social Media។",
        "lang_select": "🌐 សូមជ្រើសរើសភាសា៖", "lang_changed": "✅ បានប្តូរទៅជាភាសាខ្មែរជោគជ័យ!"
    },
    "english": {
        "welcome": "👋 Welcome to our Social Media service system!\n\n👇 Please select an option below:",
        "services": "🛍️ Services", "account": "🪪 Account", "add_fund": "💸 Add Fund", "lang": "🌐 Language",
        "contact": "📞 Contact", "about": "ℹ️ About", "back": "🔙 Back",
        "platform_select": "📌 Please select a Platform:", "fb_select": "📌 Please select Facebook service:",
        "link_prompt": "🔗 Selected package: **{package}** (Price: **${price:.2f}**)\n\n🔗 Please send your Link here:",
        "insufficient_balance": "❌ **Your balance is insufficient!**\n\n• Service price: **${price:.2f}**\n• Your balance: **${balance:.2f}**\n\nPlease click **💸 Add Fund** to top up first!",
        "success_order": "✅ Thank you! Your order has been placed and sent to Admin.",
        "add_fund_prompt": "💸 **Add Fund**\n\nPlease enter the amount you want to top up (e.g. `10` or `5.5` in USD):",
        "slip_prompt": "📸 Please send your payment Slip here for Admin review!",
        "slip_success": "✅ Thank you! Your payment slip has been sent to Admin.",
        "account_info": "🪪 **Your Account Information**\n\n• Username: {username}\n• ID: {user_id}\n• Balance: ${balance:.2f}",
        "contact_info": f"Contact Admin:\n- Telegram: {ADMIN_USERNAME}",
        "about_info": "This is an automated bot for Social Media services.",
        "lang_select": "🌐 Please select language:", "lang_changed": "✅ Switched to English successfully!"
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

    if user_id in user_states and user_states[user_id].get('step') == 'waiting_link':
        state = user_states[user_id]
        package = state.get('package')
        price = state.get('price')
        link = text
        
        if user_balances[user_id] < price:
            await update.message.reply_text(t["insufficient_balance"].format(price=price, balance=user_balances[user_id]), reply_markup=get_main_keyboard(lang), parse_mode="Markdown")
            del user_states[user_id]
            return
            
        user_balances[user_id] -= price
        await update.message.reply_text(f"{t['success_order']}\n💰 Balance: **${user_balances[user_id]:.2f}**", reply_markup=get_main_keyboard(lang), parse_mode="Markdown")
        
        admin_keyboard = [[InlineKeyboardButton("Approve", callback_data=f"approve_{user_id}"), InlineKeyboardButton("Reject", callback_data=f"reject_{user_id}")]]
        user = update.effective_user
        caption = f"🔔 **New Order!**\n\n• Service: {package}\n• Price: ${price:.2f}\n• Link: {link}\n• User: {user.first_name} (@{user.username or 'None'}) [ID: {user.id}]"
        
        try:
            await context.bot.send_message(chat_id="-1003950979639", text=caption, reply_markup=InlineKeyboardMarkup(admin_keyboard), parse_mode="Markdown")
        except Exception as e:
            print(f"Error: {e}")
        del user_states[user_id]
        return

    if user_id in user_states and user_states[user_id].get('step') == 'waiting_fund_amount':
        try:
            amount = float(text)
            if amount <= 0: raise ValueError()
            user_states[user_id] = {'step': 'waiting_fund_slip', 'amount': amount}
            await update.message.reply_text(f"✅ Amount: ${amount:.2f}\n\n{t['slip_prompt']}", reply_markup=get_main_keyboard(lang))
        except:
            await update.message.reply_text("❌ Please enter a valid number (e.g. 10):")
        return

    def process_pkg(key, name):
        price = PRICES.get(key, 0.0)
        if user_balances[user_id] < price:
            return update.message.reply_text(t["insufficient_balance"].format(price=price, balance=user_balances[user_id]), reply_markup=get_main_keyboard(lang), parse_mode="Markdown")
        user_states[user_id] = {'step': 'waiting_link', 'package': name, 'price': price}
        return update.message.reply_text(t["link_prompt"].format(package=name, price=price), reply_markup=get_main_keyboard(lang), parse_mode="Markdown")

    if text in [f"1K ~ 0.70$", f"5K ~ 3.50$", f"10K ~ 7.00$", f"15K ~ 10.50$", f"20K ~ 14.00$", f"30K ~ 21.00$", f"40K ~ 28.00$", f"50K ~ 35.00$"]:
        return await process_pkg(f"FACEBOOK FOLLOW ({text.split(' ~ ')[0]})", f"FACEBOOK FOLLOW ({text.split(' ~ ')[0]})")
    if "~ 0.80$" in text or "~ 4.00$" in text or "~ 8.00$" in text or "~ 16.00$" in text or "~ 24.00$" in text or "~ 32.00$" in text or "~ 40.00$" in text or "~ 48.00$" in text or "~ 56.00$" in text or "~ 64.00$" in text or "~ 72.00$" in text:
        return await process_pkg(f"FACEBOOK LIKE ({text.split(' ~ ')[0]})", f"FACEBOOK LIKE ({text.split(' ~ ')[0]})")
    if "~ 0.53$" in text or "~ 2.65$" in text or "~ 5.30$" in text or "~ 10.60$" in text or "~ 15.90$" in text or "~ 21.20$" in text or "~ 26.50$" in text or "~ 31.80$" in text or "~ 37.10$" in text or "~ 42.40$" in text or "~ 47.70$" in text or "~ 53.00$" in text:
        return await process_pkg(f"FACEBOOK VIEWS ({text.split(' ~ ')[0]})", f"FACEBOOK VIEWS ({text.split(' ~ ')[0]})")

    if text == t["services"]:
        await update.message.reply_text(t["platform_select"], reply_markup=ReplyKeyboardMarkup([["📘 Facebook", "🎵 TikTok"], [t["back"]]], resize_keyboard=True))
    elif text == t["account"]:
        await update.message.reply_text(t["account_info"].format(username=f"@{update.effective_user.username}" if update.effective_user.username else "None", user_id=user_id, balance=user_balances[user_id]), reply_markup=get_main_keyboard(lang), parse_mode="Markdown")
    elif text == t["add_fund"]:
        user_states[user_id] = {'step': 'waiting_fund_amount'}
        await update.message.reply_text(t["add_fund_prompt"], reply_markup=get_main_keyboard(lang), parse_mode="Markdown")
    elif text == t["lang"]:
        await update.message.reply_text(t["lang_select"], reply_markup=ReplyKeyboardMarkup([["🇰🇭 ភាសាខ្មែរ", "🇬🇧 English"], [t["back"]]], resize_keyboard=True))
    elif text in ["🇰🇭 ភាសាខ្មែរ", "🇰🇭 Khmer"]:
        user_languages[user_id] = "khmer"
        await update.message.reply_text(TEXTS["khmer"]["lang_changed"], reply_markup=get_main_keyboard("khmer"))
    elif text == "🇬🇧 English":
        user_languages[user_id] = "english"
        await update.message.reply_text(TEXTS["english"]["lang_changed"], reply_markup=get_main_keyboard("english"))
    elif text == "📘 Facebook":
        await update.message.reply_text(t["fb_select"], reply_markup=ReplyKeyboardMarkup([["👥 Facebook Follow", "👍 Facebook Like"], ["👁️ Facebook Views", t["back"]]], resize_keyboard=True))
    elif text == "👥 Facebook Follow":
        await update.message.reply_text("FACEBOOK FOLLOW:", reply_markup=ReplyKeyboardMarkup([["1K ~ 0.70$", "5K ~ 3.50$"], ["10K ~ 7.00$", "15K ~ 10.50$"], ["20K ~ 14.00$", "30K ~ 21.00$"], ["40K ~ 28.00$", "50K ~ 35.00$"], [t["back"]]], resize_keyboard=True))
    elif text == "👍 Facebook Like":
        await update.message.reply_text("FACEBOOK LIKE:", reply_markup=ReplyKeyboardMarkup([["1K ~ 0.80$", "5K ~ 4.00$"], ["10K ~ 8.00$", "20K ~ 16.00$"], ["30K ~ 24.00$", "40K ~ 32.00$"], ["50K ~ 40.00$", "60K ~ 48.00$"], ["70K ~ 56.00$", "80K ~ 64.00$"], ["90K ~ 72.00$"], [t["back"]]], resize_keyboard=True))
    elif text == "👁️ Facebook Views":
        await update.message.reply_text("FACEBOOK VIEWS:", reply_markup=ReplyKeyboardMarkup([["1K ~ 0.53$", "5K ~ 2.65$"], ["10K ~ 5.30$", "20K ~ 10.60$"], ["30K ~ 15.90$", "40K ~ 21.20$"], ["50K ~ 26.50$", "60K ~ 31.80$"], ["70K ~ 37.10$", "80K ~ 42.40$"], ["90K ~ 47.70$", "100K ~ 53.00$"], [t["back"]]], resize_keyboard=True))
    elif text == "🎵 TikTok":
        await update.message.reply_text("TikTok service coming soon!")
    elif text == t["back"]:
        await update.message.reply_text(t["welcome"], reply_markup=get_main_keyboard(lang))
    elif text == t["contact"]:
        await update.message.reply_text(t["contact_info"], parse_mode="Markdown")
    elif text == t["about"]:
        await update.message.reply_text(t["about_info"])

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    t = TEXTS[lang]
    
    if user_id in user_states and user_states[user_id].get('step') == 'waiting_fund_slip':
        amount = user_states[user_id].get('amount')
        await update.message.reply_text(t["slip_success"], reply_markup=get_main_keyboard(lang))
        
        admin_keyboard = [[InlineKeyboardButton("Approve Fund", callback_data=f"fundapprove_{user_id}_{amount}"), InlineKeyboardButton("Reject", callback_data=f"fundreject_{user_id}")]]
        user = update.effective_user
        caption = f"💸 **New Add Fund!**\n\n• Amount: ${amount:.2f}\n• User: {user.first_name} (@{user.username or 'None'}) [ID: {user.id}]"
        
        try:
            await context.bot.send_photo(chat_id="-1003950979639", photo=update.message.photo[-1].file_id, caption=caption, reply_markup=InlineKeyboardMarkup(admin_keyboard), parse_mode="Markdown")
        except Exception as e:
            print(f"Error: {e}")
        del user_states[user_id]
    else:
        await update.message.reply_text("Please use Add Fund first.")

async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    original_caption = query.message.caption or ""
    
    try:
        parts = data.split("_")
        action = parts[0]
        
        if action == "approve":
            target_user_id = int(parts[1])
            await query.edit_message_caption(caption=original_caption + "\n\nStatus: Approved ✅", parse_mode="Markdown")
            try: 
                await context.bot.send_message(chat_id=target_user_id, text="Your order has been Approved! ✅")
            except: pass
            
        elif action == "reject":
            target_user_id = int(parts[1])
            await query.edit_message_caption(caption=original_caption + "\n\nStatus: Rejected ❌", parse_mode="Markdown")
            try: 
                await context.bot.send_message(chat_id=target_user_id, text="Your order has been Rejected. ❌")
            except: pass
            
        elif action == "fundapprove":
            target_user_id = int(parts[1])
            amount = float(parts[2])
            
            if target_user_id not in user_balances:
                user_balances[target_user_id] = 0.00
            user_balances[target_user_id] += amount
            
            await query.edit_message_caption(caption=original_caption + f"\n\nStatus: Approved ✅ (+${amount:.2f})", parse_mode="Markdown")
            try: 
                await context.bot.send_message(
                    chat_id=target_user_id, 
                    text=f"🎉 Admin approved your top-up of **${amount:.2f}**!\n💰 Balance: **${user_balances[target_user_id]:.2f}**", 
                    parse_mode="Markdown"
                )
            except: pass
            
        elif action == "fundreject":
            target_user_id = int(parts[1])
            await query.edit_message_caption(caption=original_caption + "\n\nStatus: Rejected ❌", parse_mode="Markdown")
            try: 
                await context.bot.send_message(chat_id=target_user_id, text="❌ Top-up request rejected.")
            except: pass
            
    except Exception as e:
        print(f"Error in admin_callback: {e}")

if __name__ == "__main__":
    TOKEN = "8675478122:AAFem3pCVLz_zZBebYuRmWcKGFAR1FBGY5Y"
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(CallbackQueryHandler(admin_callback))
    print("Bot is running...")
    app.run_polling()
