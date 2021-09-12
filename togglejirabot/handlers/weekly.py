import logging

from telegram import ParseMode, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler)

from togglejirabot.decorators import security
from togglejirabot.toggle.togglereport import ToggleReport

from .keyboard import weekly_keyboard_markup

ANSWER = range(0)


@security
def weekly_conversion(update: Update, context: CallbackContext):
    logging.info('weekly_conversion')
    reply_markup = weekly_keyboard_markup()

    update.message.reply_text('Please choose: ', reply_markup=reply_markup)
    return ANSWER


def weekly_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'this':
        message = ToggleReport().week()
    else:
        message = ToggleReport().last_week()

    query.edit_message_text(text=f"Create report for {query.data} week.")
    update.effective_chat.send_message(message, parse_mode=ParseMode.HTML)

    return ConversationHandler.END


def weekly_conversation_handler():
    return ConversationHandler(
        entry_points=[CommandHandler('weekly', weekly_conversion)],
        states={
            ANSWER: [CallbackQueryHandler(weekly_callback)]
        },
        fallbacks=[]
    )
