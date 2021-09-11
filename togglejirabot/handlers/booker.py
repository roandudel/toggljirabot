import logging

from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from togglejirabot.decorators import security
from togglejirabot.toggle.booker import ToggleReportBookerReport
from togglejirabot.toggle.togglereport import ToggleReport


@security
def command_booker(update: Update, context: CallbackContext):
    logging.info('booker')
    message = ToggleReport(message_preparer=ToggleReportBookerReport()).week()
    update.effective_chat.send_message(message, parse_mode=ParseMode.HTML)


@security
def command_last_week_booker(update: Update, context: CallbackContext):
    logging.info('booker')
    message = ToggleReport(message_preparer=ToggleReportBookerReport()).last_week()
    update.effective_chat.send_message(message, parse_mode=ParseMode.HTML)
