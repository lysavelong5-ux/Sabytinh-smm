import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import os
import time

# យក Token ពី Environment Variables
TOKEN = os.environ.get('BOT_TOKEN', 'ដាក់_TOKEN_របស់អ្នកនៅទីនេះ')
bot = telebot.TeleBot(TOKEN)

user_languages = {}

texts = {
    'kh': {
        'welcome': "សួស្តី {name}! សូមជ្រើសរើសសេវាកម្មខាងក្រោម៖",
        'select_below': "👇 សូមជ្រើសរើសជម្រើសនៅខាងក្រោម៖",
        'btn_manage': "👨🏻‍💻 គ្រប់គ្រងគណនី",
        'btn_rent': "🛍 ជួលសេវាកម្ម / ទិញ",
        'btn_change_lang_inline': "🇬🇧",
        'manage_text': "នេះគឺជាទំព័រសម្រាប់ គ្រប់គ្រងគណនី របស់អ្នក។",
        'rent_menu_text': "សូមជ្រើសរើសសេវាកម្មដែលអ្នកចង់បានខាងក្រោម៖",
        'btn_bot_smm': "🤖 BOT SMM",
        'btn_robux': "🎮 ទិញ Robux",
        'btn_back': "🔙 ត្រឡប់ក្រោយ",
        
        # ផ្នែក BOT SMM
        'bot_smm_text': "តារាងសម្រាប់លោកអ្នកជួល Telegram bot តម្លៃ :",
        'package_selected': "អ្នកបានជ្រើសរើសកញ្ចប់ {package} ។\n\n👇 សូមផ្ញើ API TOKEN BOT និង KHQR CODE របស់អ្នកមកកាន់យើងខ្ញុំ៖",
        'data_received': "✅ ទទួលបានទិន្នន័យជោគជ័យ!\n\nសូមរង់ចាំការបញ្ជាក់ពី Admin របស់យើងខ្ញុំ។",
        
        # ផ្នែក Robux
        'rob
