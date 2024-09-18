import sqlite3

from telegram.ext import CallbackContext, ContextTypes, ConversationHandler

from keyboard.inline_keyboard import *
from telegram import Update, Location, Contact, ReplyKeyboardRemove
from keyboard.inline_keyboard import location_shop_keyboard

NAME, CHAT_ID = range(2)


async def menu_handler(update: Update, context):
    reply_markup = InlineKeyboardMarkup(state_inline)
    await update.message.reply_text("👇Qaysi davlat shokalatlari sizga kerak👇", reply_markup=reply_markup)


async def location_shop(update: Update, context):
    reply_markup = InlineKeyboardMarkup(location_shop_keyboard)
    await update.message.reply_text("Manzilimz📍", reply_markup=reply_markup)


async def settings(update: Update, context):
    await update.message.reply_text("Salom")


async def my_information(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT name, phone_number, latitude, longitude FROM users WHERE chat_id = ?', (chat_id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        name, phone_number, latitude, longitude = result
        await update.message.reply_text(f"✍️Ismingiz: {name}\n"
                                        f"📞Raqamingiz: {phone_number}\n"
                                        f"📍Bu sizning saqlangan manzilingiz👇")
        await update.message.reply_location(latitude=latitude, longitude=longitude)
    else:
        await update.message.reply_text("Sizning manzilingiz topilmadi, iltimos avval manzilni yuboring.")


async def admin_add(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id == 5440011091:
        await update.message.reply_text("Assalomu aleykum qoshmohchi bolgan admingizni Ismini kiriting")
        return NAME
    else:
        await update.message.reply_text("Siz admin emasiz ")


async def admin_get_name(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Ism qabul qilindi, chat id ni kiriting")
    return CHAT_ID


async def admin_get_chat_id(update: Update, context: CallbackContext):
    context.user_data['chat_id'] = update.message.text

    name = context.user_data['name']
    chat_id = context.user_data['chat_id']
    conn = None
    try:
        conn = sqlite3.connect('bot_users.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO admins (name, chat_id) 
                              VALUES (?, ?)''', (name, chat_id))
        conn.commit()
    except sqlite3.Error as e:
        await update.message.reply_text(f"Xatolik yuz berdi: {e}")
    finally:
        if conn:
            conn.close()

    await update.message.reply_text("Chat id qoshildi, admin tayyorlandi")
    return ConversationHandler.END






async def admin_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Suhbat bekor qilindi.")
    return ConversationHandler.END
