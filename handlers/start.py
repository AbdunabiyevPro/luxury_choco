from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup
from telegram.ext import ContextTypes, filters, CallbackContext
from keyboard.default_keyboard import *
from keyboard.inline_keyboard import *
from telegram import Update, Location, Contact
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import sqlite3


from telegram.ext import ConversationHandler



NAME, LOCATION, PHONE = range(3)


async def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    reply_markup = main_keyboard


    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT chat_id FROM users WHERE chat_id = ?
    ''', (chat_id,))
    user = cursor.fetchone()

    if user is not None:
        await update.message.reply_text("Siz allaqachon ro'yxatdan o'tgansiz!",reply_markup=reply_markup)
    else:
        await update.message.reply_text('Salom, Ismingini kiriting')
        return NAME






async def name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['chat_id'] = update.message.chat_id
    context.user_data['name'] = update.message.text
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton("Lokatsiya yuborish", request_location=True)]],
                                       resize_keyboard=True)
    await update.message.reply_text("Rahmat iltmos lakatsyangizni yuboring", reply_markup=reply_markup)
    return LOCATION


async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_location: Location = update.message.location
    context.user_data['location'] = (user_location.latitude, user_location.longitude)
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton("Raqam yuborish", request_contact=True)]],
                                       resize_keyboard=True)
    await update.message.reply_text(
        f"Qabul qilindi! telefon raqamingizni yuboring.",
        reply_markup=reply_markup)
    return PHONE


async def phone_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_contact: Contact = update.message.contact
    context.user_data['phone_number'] = user_contact.phone_number

    name = context.user_data['name']
    latitude, longitude = context.user_data['location']
    phone_number = context.user_data['phone_number']
    chat_id = context.user_data['chat_id']

    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (name, chat_id, latitude, longitude, phone_number)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, chat_id, latitude, longitude, phone_number))
    conn.commit()
    conn.close()

    await update.message.reply_text(
        f"Ma'lumotlaringiz:\nIsm: {name}\nLokatsiya: {latitude, longitude}\nTelefon raqam: {phone_number}. Rahmat!",
        reply_markup=main_keyboard)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Suhbat bekor qilindi.")
    return ConversationHandler.END
