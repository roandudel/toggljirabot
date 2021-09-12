import logging

from telegram import ParseMode, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler)

from togglejirabot.decorators import security
from togglejirabot.toggle.booker import ToggleReportBookerReport
from togglejirabot.toggle.togglereport import ToggleReport

from .keyboard import weekly_keyboard_markup

ANSWER = range(1)


@security
def booker_conversation(update: Update, context: CallbackContext):
    logging.info('booker_conversation')
    reply_markup = weekly_keyboard_markup()

    update.message.reply_text('Please choose: ', reply_markup=reply_markup)
    return ANSWER


def booker_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'this':
        message = ToggleReport(message_preparer=ToggleReportBookerReport()).week()
    else:
        message = ToggleReport(message_preparer=ToggleReportBookerReport()).last_week()

    query.edit_message_text(text=f"Create report for {query.data} week.")
    update.effective_chat.send_message(message, parse_mode=ParseMode.HTML)

    return ConversationHandler.END


def booker_conversation_handler():
    return ConversationHandler(
        entry_points=[CommandHandler('booker', booker_conversation)],
        states={
            ANSWER: [CallbackQueryHandler(booker_callback)]
        },
        fallbacks=[]
    )
