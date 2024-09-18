from handlers.start import *
from handlers.products import *
from handlers.country import *
from handlers.menu import *
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, \
    filters
from handlers.start import start, name_handler, location_handler, phone_handler, cancel
from handlers.menu import menu_handler
from handlers.products import add_product, product_name, product_description, product_price, product_stock, \
    product_country, product_image, product_cancel
from handlers.upload_user_informations import upload_name_handler, upload_phone_handler, upload_location_handler, \
    upload_cancel, upload_start


def main() -> None:
    application = Application.builder().token('6325417200:AAGdSZCLozdsRhTEneaezdJdvRJHsSPm6vw').build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            0: [MessageHandler(filters.TEXT & (~filters.COMMAND), name_handler)],
            1: [MessageHandler(filters.LOCATION, location_handler)],
            2: [MessageHandler(filters.CONTACT, phone_handler)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.Text(["Menu🍫🍭", ]) & ~filters.COMMAND, menu_handler))
    application.add_handler(MessageHandler(filters.Text(["Manzil📍", ]) & ~filters.COMMAND, location_shop))
    application.add_handler(MessageHandler(filters.Text(["Mening malumotlarim👤", ]) & ~filters.COMMAND, my_information))

    application.add_handler(CallbackQueryHandler(product_italy, pattern='italy'))
    application.add_handler(CallbackQueryHandler(product_germany, pattern='germany'))
    application.add_handler(CallbackQueryHandler(product_angliya, pattern='angliya'))
    application.add_handler(CallbackQueryHandler(product_shvetsariya, pattern='shvetsariya'))
    application.add_handler(CallbackQueryHandler(product_turkiya, pattern='turkiya'))
    application.add_handler(CallbackQueryHandler(product_usa, pattern='amerika'))
    application.add_handler(CallbackQueryHandler(product_belgiya, pattern='belgiya'))

    product_handler = ConversationHandler(
        entry_points=[CommandHandler('add_product', add_product)],
        states={
            0: [MessageHandler(filters.TEXT & (~filters.COMMAND), product_name)],
            1: [MessageHandler(filters.TEXT & (~filters.COMMAND), product_description)],
            2: [MessageHandler(filters.TEXT & (~filters.COMMAND), product_price)],
            3: [MessageHandler(filters.TEXT & (~filters.COMMAND), product_stock)],
            4: [MessageHandler(filters.TEXT & (~filters.COMMAND), product_country)],
            5: [MessageHandler(filters.PHOTO & (~filters.COMMAND), product_image)]
        },
        fallbacks=[CommandHandler('cancel', product_cancel)]
    )
    admin_handler = ConversationHandler(
        entry_points=[CommandHandler('add_admin', admin_add)],
        states={
            0: [MessageHandler(filters.TEXT & (~filters.COMMAND), admin_get_name)],
            1: [MessageHandler(filters.TEXT & (~filters.COMMAND), admin_get_chat_id)]
        },
        fallbacks=[CommandHandler('cancel', admin_cancel)]
    )

    upload_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('upload_start', upload_start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, upload_name_handler)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, upload_location_handler)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, upload_phone_handler)],
        },
        fallbacks=[CommandHandler('cancel', upload_cancel)]
    )

    application.add_handler(conv_handler)
    application.add_handler(admin_handler)
    application.add_handler(product_handler)
    application.add_handler(upload_conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
