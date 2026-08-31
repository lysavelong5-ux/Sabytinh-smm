from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # បង្កើត Button ស្ថិតនៅខាងក្រោមប្រអប់សរសេរសារ
    keyboard = [
        ["ជំនួយ (Help)", "ទំនាក់ទំនង (Contact)"],
        ["ព័ត៌មាន (About)"]
    ]
    # resize_keyboard=True ជួយឱ្យប៊ូតុងមិនសូវធំខ្លាំងពេកនៅលើអេក្រង់ទូរសព្ទ
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text("សួស្តី! សូមជ្រើសរើសជម្រើសខាងក្រោម៖", reply_markup=reply_markup)

if __name__ == "__main__":
    TOKEN = "8675478122:AAFem3pCVLz_zZBebYuRmWcKGFAR1FBGY5Y"
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("Bot កំពុងដំណើរការ...")
    app.run_polling()
