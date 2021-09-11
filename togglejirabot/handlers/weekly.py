import logging

from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from togglejirabot.decorators import security
from togglejirabot.toggle.togglereport import ToggleReport


@security
def command_weekly(update: Update, context: CallbackContext):
    logging.info('weekly')
    message = ToggleReport().week()

    update.effective_chat.send_message(message, parse_mode=ParseMode.HTML)

@security
def command_last_week(update: Update, context: CallbackContext):
    logging.info('last_week')
    message = ToggleReport().last_week()

    update.effective_chat.send_message(message, parse_mode=ParseMode.HTML)
