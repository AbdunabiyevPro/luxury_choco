from telegram import ReplyKeyboardMarkup, KeyboardButton


main_keyboard = ReplyKeyboardMarkup(
        [
            [KeyboardButton("Menu🍫🍭"), KeyboardButton("Mening malumotlarim👤"),],
            [KeyboardButton("Sozlamalar⚙️"), KeyboardButton("Manzil📍")]
        ],resize_keyboard=True
    )


phone_number_keyboard = [
    [KeyboardButton("Telefon raqam☎️", request_contact=True)]
]

location_keyboard = [
    [KeyboardButton(text="Lokatsiya yuborish", request_location=True)]
]



def states():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("Italy 🇮🇹"),KeyboardButton("Germany🇩🇪")],
            [KeyboardButton("Angliya🇬🇧"),KeyboardButton("Shvetsariya🇨🇭")],
            [KeyboardButton("Turkiya🇹🇷"),KeyboardButton("Usa🇺🇸")],
            [KeyboardButton("Belgiya🇧🇪")]
        ],resize_keyboard=True
    )





admin_main_keyboard = ReplyKeyboardMarkup(
        [
            [KeyboardButton("Menu🍫🍭"), KeyboardButton("Mening malumotlarim👤"),],
            [KeyboardButton("Sozlamalar⚙️"), KeyboardButton("Manzil📍")]
        ],resize_keyboard=True
    )