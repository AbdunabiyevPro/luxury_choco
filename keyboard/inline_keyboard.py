from telegram import InlineKeyboardMarkup, InlineKeyboardButton

state_inline = [
    [InlineKeyboardButton("Italy 🇮🇹", callback_data="italy")],
    [InlineKeyboardButton("Germany 🇩🇪", callback_data='germany')],
    [InlineKeyboardButton("Angliya🇬🇧", callback_data='angliya')],
    [InlineKeyboardButton("Shvetsariya🇨🇭", callback_data='shvetsariya')],
    [InlineKeyboardButton("Turkiya🇹🇷", callback_data='turkiya')],
    [InlineKeyboardButton("Usa🇺🇸", callback_data='amerika')],
    [InlineKeyboardButton("Belgiya🇧🇪", callback_data='belgiya')]
]

location_shop_keyboard = [
    [InlineKeyboardButton("Manzil📍", url="https://maps.app.goo.gl/pDkhsdVSSEWyncxg9")]
]
