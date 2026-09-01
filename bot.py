from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

user_states = {}
user_balances = {}  # សម្រាប់រក្សាទុកទឹកប្រាក់ (Balance) របស់អតិថិជនម្នាក់ៗ

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "Welcome to our Social Media service system!\n\n"
        "Here you can order Facebook services easily and quickly.\n\n"
        "Please select an option below:"
    )
    keyboard = [
        ["🛍️ Services", "🪪 Account"],
        ["Contact", "About"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    # ពិនិត្យមើលទឹកប្រាក់របស់ User ຖ້າទើបចូលប្រើលើកដំបូងកំណត់ជា 0.00$
    if user_id not in user_balances:
        user_balances[user_id] = 0.00$ if "0.00$" else 0.00

    if user_id in user_states and user_states[user_id].get('step') == 'waiting_link':
        state = user_states[user_id]
        state['link'] = text
        state['step'] = 'waiting_slip'
        
        keyboard = [
            ["🛍️ Services", "🪪 Account"],
            ["Contact", "About"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        qr_url = "https://cdn.phototourl.com/free/2026-09-01-1a3cfec5-d60d-4038-b50c-ac83f71acab2.jpg"
        caption = (
            "Link received successfully!\n\n"
            "Please scan the QR Code above to make payment:\n\n"
            "After payment, please send your payment Slip here!"
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
            await update.message.reply_text(caption, reply_markup=reply_markup)
        return

    if text in ["1K ~ 0.70$", "5K ~ 3.50$", "10K ~ 7.00$", "15K ~ 10.50$", "20K ~ 14.00$", "30K ~ 21.00$", "40K ~ 28.00$", "50K ~ 35.00$"]:
        package_name = text.split(" ~ ")[0]
        user_states[user_id] = {
            'step': 'waiting_link',
            'package': f"FACEBOOK FOLLOW ({package_name})"
        }
        keyboard = [
            ["🛍️ Services", "🪪 Account"],
            ["Contact", "About"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(f"You selected: FACEBOOK FOLLOW ({package_name})\n\nPlease send your Facebook Link:", reply_markup=reply_markup)
        return

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
            ["🛍️ Services", "🪪 Account"],
            ["Contact", "About"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(f"You selected: FACEBOOK LIKE ({package_name})\n\nPlease send your Facebook Link:", reply_markup=reply_markup)
        return

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
            ["🛍️ Services", "🪪 Account"],
            ["Contact", "About"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(f"You selected: FACEBOOK VIEWS ({package_name})\n\nPlease send your Facebook Link:", reply_markup=reply_markup)
        return

    if text == "🛍️ Services":
        keyboard = [
            ["📘 Facebook", "🎵 TikTok"],
            ["🔙 Back"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Please select a Platform:", reply_markup=reply_markup)
        
    elif text == "🪪 Account":
        user = update.effective_user
        username = f"@{user.username}" if user.username else "No Username"
        balance = user_balances.get(user_id, 0.00)
        
        account_info = (
            "🪪 **Account Information**\n\n"
            f"• Username: {username}\n"
            f"• ID: {user.id}\n"
            f"• Balance: ${balance:.2f}"
        )
        keyboard = [
            ["🛍️ Services", "🪪 Account"],
            ["Contact", "About"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(account_info, reply_markup=reply_markup, parse_mode="Markdown")

    elif text == "📘 Facebook":
        keyboard = [
            ["👥 Facebook Follow", "👍 Facebook Like"],
            ["👁️ Facebook Views", "🔙 Back"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Please select Facebook service:", reply_markup=reply_markup)
        
    elif text == "👥 Facebook Follow":
        price_keyboard = [
            ["1K ~ 0.70$", "5K ~ 3.50$"],
            ["10K ~ 7.00$", "15K ~ 10.50$"],
            ["20K ~ 14.00$", "30K ~ 21.00$"],
            ["40K ~ 28.00$", "50K ~ 35.00$"],
            ["🔙 Back"]
        ]
        reply_markup = ReplyKeyboardMarkup(price_keyboard, resize_keyboard=True)
        await update.message.reply_text("Please select FACEBOOK FOLLOW package:", reply_markup=reply_markup)

    elif text == "👍 Facebook Like":
        price_keyboard = [
            ["1K ~ 0.80$", "5K ~ 4.00$"],
            ["10K ~ 8.00$", "20K ~ 16.00$"],
            ["30K ~ 24.00$", "40K ~ 32.00$"],
            ["50K ~ 40.00$", "60K ~ 48.00$"],
            ["70K ~ 56.00$", "80K ~ 64.00$"],
            ["90K ~ 72.00$"],
            ["🔙 Back"]
        ]
        reply_markup = ReplyKeyboardMarkup(price_keyboard, resize_keyboard=True)
        await update.message.reply_text("Please select FACEBOOK LIKE package:", reply_markup=reply_markup)

    elif text == "👁️ Facebook Views":
        price_keyboard = [
            ["1K ~ 0.53$", "5K ~ 2.65$"],
            ["10K ~ 5.30$", "20K ~ 10.60$"],
            ["30K ~ 15.90$", "40K ~ 21.20$"],
            ["50K ~ 26.50$", "60K ~ 31.80$"],
            ["70K ~ 37.10$", "80K ~ 42.40$"],
            ["90K ~ 47.70$", "100K ~ 53.00$"],
            ["🔙 Back"]
        ]
        reply_markup = ReplyKeyboardMarkup(price_keyboard, resize_keyboard=True)
        await update.message.reply_text("Please select FACEBOOK VIEWS package:", reply_markup=reply_markup)

    elif text == "🎵 TikTok":
        await update.message.reply_text("TikTok service is coming soon!")

    elif text == "🔙 Back":
        keyboard = [
            ["🛍️ Services", "🪪 Account"],
            ["Contact", "About"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Please select an option below:", reply_markup=reply_markup)
        
    elif text == "Contact":
        await update.message.reply_text("Contact Admin: @YourUsername")
        
    elif text == "About":
        await update.message.reply_text("This is an automated SMM service bot.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id in user_states and user_states[user_id].get('step') == 'waiting_slip':
        state = user_states[user_id]
        package = state.get('package')
        link = state.get('link')
        
        photo_file_id = update.message.photo[-1].file_id
        
        keyboard = [
            ["🛍️ Services", "🪪 Account"],
            ["Contact", "About"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text("Thank you! Your order and payment slip have been sent to Admin.", reply_markup=reply_markup)
        
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
            print(f"Error sending photo notification: {e}")
            
        del user_states[user_id]
    else:
        await update.message.reply_text("Please select a service from the menu first.")

async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    original_caption = query.message.caption or ""
    
    action, target_user_id = data.split("_")
    target_user_id = int(target_user_id)
    
    if action == "approve":
        new_caption = original_caption + "\n\nStatus: Approved"
        await query.edit_message_caption(caption=new_caption, parse_mode="Markdown")
        
        try:
            await context.bot.send_message(
                chat_id=target_user_id,
                text="Your order has been Approved by Admin!",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Error notifying user: {e}")
            
    elif action == "reject":
        new_caption = original_caption + "\n\nStatus: Rejected"
        await query.edit_message_caption(caption=new_caption, parse_mode="Markdown")
        
        try:
            await context.bot.send_message(
                chat_id=target_user_id,
                text="Your order has been Rejected by Admin.",
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
    
    print("Bot is running...")
    app.run_polling()
