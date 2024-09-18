import requests
from telegram import Update, Location, Contact, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import sqlite3
import os
from telegram.ext import ConversationHandler
from keyboard.default_keyboard import states
from keyboard.default_keyboard import main_keyboard


NAME, DESCRIPTION, PRICE, STOCK, COUNTRY, IMAGE_PATH = range(6)


async def add_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    reply_markup = main_keyboard
    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()
    cursor.execute(''' SELECT name, chat_id FROM admins WHERE chat_id = ? ''', (chat_id,))
    user = cursor.fetchone()

    if user is not None or chat_id == 5440011091:
        await update.message.reply_text("Assalomu aleykum admin, productni ismini kiritng")
        return NAME
    else:
        await update.message.reply_text("Siz admin emassiz")



async def product_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Ism qabul qilindi. Mahsulot haqida ma'lumot kiriting:")
    return DESCRIPTION


async def product_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['description'] = update.message.text
    await update.message.reply_text("Ma'lumot qabul qilindi. Mahsulot narhini kiriting:")
    return PRICE


async def product_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['price'] = update.message.text
    await update.message.reply_text("Narx qabul qilindi. Mahsulot zaxirasini kiriting:")
    return STOCK


async def product_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['stock'] = update.message.text
    replay_markup = states()
    await update.message.reply_text("Mahsulot shaharini yuboring:", reply_markup=replay_markup)
    return COUNTRY


async def product_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    replay_markup = ReplyKeyboardRemove()
    context.user_data['country'] = update.message.text
    await update.message.reply_text("Shahar qabul qilindi. Mahsulot rasmini yuboring",reply_markup=replay_markup)
    return IMAGE_PATH


async def product_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    new_file = await context.bot.get_file(photo.file_id)
    reply_keyboard = main_keyboard

    folder_path = 'photos'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    image_path = os.path.join(folder_path, f"{photo.file_id}.jpg")
    print(image_path)
    await new_file.download_to_drive(image_path)

    name = context.user_data['name']
    description = context.user_data['description']
    price = context.user_data['price']
    stock = context.user_data['stock']
    country = context.user_data['country']
    context.user_data['image_path'] = image_path

    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()

    a = cursor.execute('''INSERT INTO products (name, description, price, stock, country, image_path) 
                      VALUES (?, ?, ?, ?, ?, ?)''', (name, description, price, stock, country, image_path))
    conn.commit()
    conn.close()

    await update.message.reply_text("Ma'lumotlaringiz saqlandi", reply_markup=reply_keyboard)
    return ConversationHandler.END


async def product_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_markup = ReplyKeyboardRemove()
    await update.message.reply_text("Suhbat bekor qilindi.", reply_markup=reply_markup)
    return ConversationHandler.END


# get italy products

def get_italy_products():
    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()

    try:
        # cursor.execute('SELECT id, name, description, price, stock, image_path FROM products WHERE country = uzb')
        cursor.execute('''SELECT id, name, description, price, stock, image_path 
                          FROM products WHERE country = ?''', ('Italy 🇮🇹',))
        products = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Ma'lumotlar bazasida xato: {e}")
        products = []
    finally:
        conn.close()

    return products


async def product_italy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = get_italy_products()
    chat_id = update.effective_chat.id
    if products:
        for product in products:
            keys = ['image_path', 'name', 'description', 'price', 'stock']
            product_dict = dict(zip(keys, product))
            message = (f"✍️Nomi: {product_dict['name']}\n"
                       f"🗓Tavsifi: {product_dict['description']}\n"
                       f"💵Narxi: {product_dict['price']}so'm\n"
                       f"🍬Zaxira: {product_dict['stock']}qoldi\n")
            image_path = product[5]

            with open(image_path, 'rb') as image_file:
                await context.bot.send_photo(chat_id=chat_id, photo=image_file, caption=message)

    else:
        await update.message.reply_text("Mahsulotlar topilmadi.")





# get germany products





def get_germany_products():
    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()

    try:
        # cursor.execute('SELECT id, name, description, price, stock, image_path FROM products WHERE country = uzb')
        cursor.execute('''SELECT id, name, description, price, stock, image_path 
                          FROM products WHERE country = ?''', ('Germany🇩🇪',))
        products = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Ma'lumotlar bazasida xato: {e}")
        products = []
    finally:
        conn.close()

    return products






async def product_germany(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = get_germany_products()
    print(products)
    chat_id = update.effective_chat.id
    if products:
        for product in products:
            keys = ['image_path', 'name', 'description', 'price', 'stock']
            product_dict = dict(zip(keys, product))
            message = (f"Nomi: {product_dict['name']}\n"
                       f"Tavsifi: {product_dict['description']}\n"
                       f"Narxi: {product_dict['price']}so'm\n"
                       f"Zaxira: {product_dict['stock']}qoldi\n")
            image_path = product[5]
            print(image_path)
            with open(image_path, 'rb') as image_file:
                await context.bot.send_photo(chat_id=chat_id, photo=image_file, caption=message)
    else:
        await update.message.reply_text("Mahsulotlar topilmadi.")


# get angliya products

def get_angliya_products():
    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()

    try:
        # cursor.execute('SELECT id, name, description, price, stock, image_path FROM products WHERE country = uzb')
        cursor.execute('''SELECT id, name, description, price, stock, image_path 
                          FROM products WHERE country = ?''', ('Angliya🇬🇧',))
        products = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Ma'lumotlar bazasida xato: {e}")
        products = []
    finally:
        conn.close()

    return products


async def product_angliya(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = get_angliya_products()
    print(products)
    chat_id = update.effective_chat.id
    if products:
        for product in products:
            keys = ['image_path', 'name', 'description', 'price', 'stock']
            product_dict = dict(zip(keys, product))
            message = (f"Nomi: {product_dict['name']}\n"
                       f"Tavsifi: {product_dict['description']}\n"
                       f"Narxi: {product_dict['price']}so'm\n"
                       f"Zaxira: {product_dict['stock']}qoldi\n")
            image_path = product[5]
            print(image_path)
            with open(image_path, 'rb') as image_file:
                await context.bot.send_photo(chat_id=chat_id, photo=image_file, caption=message)
    else:
        await update.message.reply_text("Mahsulotlar topilmadi.")



# get shvetsariya products

def get_shvetsariya_products():
    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()

    try:
        # cursor.execute('SELECT id, name, description, price, stock, image_path FROM products WHERE country = uzb')
        cursor.execute('''SELECT id, name, description, price, stock, image_path 
                          FROM products WHERE country = ?''', ('Shvetsariya🇨🇭',))
        products = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Ma'lumotlar bazasida xato: {e}")
        products = []
    finally:
        conn.close()

    return products


async def product_shvetsariya(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = get_shvetsariya_products()
    print(products)
    chat_id = update.effective_chat.id
    if products:
        for product in products:
            keys = ['image_path', 'name', 'description', 'price', 'stock']
            product_dict = dict(zip(keys, product))
            message = (f"Nomi: {product_dict['name']}\n"
                       f"Tavsifi: {product_dict['description']}\n"
                       f"Narxi: {product_dict['price']}so'm\n"
                       f"Zaxira: {product_dict['stock']}qoldi\n")
            image_path = product[5]
            print(image_path)
            with open(image_path, 'rb') as image_file:
                await context.bot.send_photo(chat_id=chat_id, photo=image_file, caption=message)
    else:
        await update.message.reply_text("Mahsulotlar topilmadi.")




# get turkiya products

def get_turkiya_products():
    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()

    try:
        # cursor.execute('SELECT id, name, description, price, stock, image_path FROM products WHERE country = uzb')
        cursor.execute('''SELECT id, name, description, price, stock, image_path 
                          FROM products WHERE country = ?''', ('Turkiya🇹🇷',))
        products = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Ma'lumotlar bazasida xato: {e}")
        products = []
    finally:
        conn.close()

    return products


async def product_turkiya(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = get_turkiya_products()
    print(products)
    chat_id = update.effective_chat.id
    if products:
        for product in products:
            keys = ['image_path', 'name', 'description', 'price', 'stock']
            product_dict = dict(zip(keys, product))
            message = (f"Nomi: {product_dict['name']}\n"
                       f"Tavsifi: {product_dict['description']}\n"
                       f"Narxi: {product_dict['price']}so'm\n"
                       f"Zaxira: {product_dict['stock']}qoldi\n")
            image_path = product[5]
            print(image_path)
            with open(image_path, 'rb') as image_file:
                await context.bot.send_photo(chat_id=chat_id, photo=image_file, caption=message)
    else:
        await update.message.reply_text("Mahsulotlar topilmadi.")







# get usa products

def get_usa_products():
    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()

    try:
        # cursor.execute('SELECT id, name, description, price, stock, image_path FROM products WHERE country = uzb')
        cursor.execute('''SELECT id, name, description, price, stock, image_path 
                          FROM products WHERE country = ?''', ('Usa🇺🇸',))
        products = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Ma'lumotlar bazasida xato: {e}")
        products = []
    finally:
        conn.close()

    return products


async def product_usa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = get_usa_products()
    print(products)
    chat_id = update.effective_chat.id
    if products:
        for product in products:
            keys = ['image_path', 'name', 'description', 'price', 'stock']
            product_dict = dict(zip(keys, product))
            message = (f"Nomi: {product_dict['name']}\n"
                       f"Tavsifi: {product_dict['description']}\n"
                       f"Narxi: {product_dict['price']}so'm\n"
                       f"Zaxira: {product_dict['stock']}qoldi\n")
            image_path = product[5]
            print(image_path)
            with open(image_path, 'rb') as image_file:
                await context.bot.send_photo(chat_id=chat_id, photo=image_file, caption=message)
    else:
        await update.message.reply_text("Mahsulotlar topilmadi.")


# get belgiya products

def get_belgiya_products():
    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()

    try:
        # cursor.execute('SELECT id, name, description, price, stock, image_path FROM products WHERE country = uzb')
        cursor.execute('''SELECT id, name, description, price, stock, image_path 
                          FROM products WHERE country = ?''', ('Belgiya🇧🇪',))
        products = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Ma'lumotlar bazasida xato: {e}")
        products = []
    finally:
        conn.close()

    return products


async def product_belgiya(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = get_belgiya_products()
    print(products)
    chat_id = update.effective_chat.id
    if products:
        for product in products:
            keys = ['image_path', 'name', 'description', 'price', 'stock']
            product_dict = dict(zip(keys, product))
            message = (f"Nomi: {product_dict['name']}\n"
                       f"Tavsifi: {product_dict['description']}\n"
                       f"Narxi: {product_dict['price']}so'm\n"
                       f"Zaxira: {product_dict['stock']}qoldi\n")
            image_path = product[5]
            print(image_path)
            with open(image_path, 'rb') as image_file:
                await context.bot.send_photo(chat_id=chat_id, photo=image_file, caption=message)
    else:
        await update.message.reply_text("Mahsulotlar topilmadi.")


