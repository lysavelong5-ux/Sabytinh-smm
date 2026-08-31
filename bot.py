import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("ចុចទីនេះដើម្បីទៅកាន់ Google", url="https://www.google.com")],
        [InlineKeyboardButton("ចុចទីនេះដើម្បីទាក់ទងមកខ្ញុំ", callback_data="btn_click")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("សួស្តី! នេះគឺជា Bot ដែលមាន Button៖", reply_markup=reply_markup)

if __name__ == "__main__":
    TOKEN = "8675478122:AAFem3pCVLz_zZBebYuRmWcKGFAR1FBGY5Y"
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("Bot កំពុងដំណើរការ...")
    app.run_polling()
