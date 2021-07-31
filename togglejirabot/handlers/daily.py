import logging

from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from togglejirabot.decorators import security
from togglejirabot.toggle.togglereport import ToggleReport


@security
def command_daily(update: Update, context: CallbackContext):
    logging.info('daily')
    toggle_report = ToggleReport().today()

    update.effective_chat.send_message(toggle_report, parse_mode=ParseMode.HTML)
