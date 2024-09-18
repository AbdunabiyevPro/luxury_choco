from telegram import Update, Location, Contact
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import sqlite3
import os
from telegram.ext import ConversationHandler

ID, NAME = range(2)


async def country_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Shahar id sini kiriting")
    return ID


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['id'] = update.message.id
    await update.message.reply_text("id qabul qilindi! shahar nomini kiriting")
    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.id

    id = context.user_data['id']
    name = context.user_data['name']

    conn = sqlite3.connect('bot_user.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO countries (id, name)
        VALUES (?,?)
    ''', (id, name))
    conn.commit()
    conn.close()

    await update.message.reply_text('shahar nomi qabul qilindi')
    return ConversationHandler.END




async def country_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Suhbat bekor qilindi.")
    return ConversationHandler.END