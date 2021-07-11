import logging

from telegram import Update
from telegram.ext import CallbackContext

from togglejirabot.decorators import security


@security
def command_start(update: Update, context: CallbackContext):
    logging.info("START is calling")
    message = f'Chat-ID: {update.effective_chat.id}'

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
