import logging

from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from togglejirabot.decorators import security
from togglejirabot.toggle.model.togglereport import ToggleReport


@security
def command_weekly(update: Update, context: CallbackContext):
    logging.info('weekly')
    message = ToggleReport().week()

    update.effective_chat.send_message(message, parse_mode=ParseMode.HTML)
