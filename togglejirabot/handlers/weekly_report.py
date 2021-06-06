from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from togglejirabot.decorators import security


@security
def command_weekly(update: Update, context: CallbackContext):
    message = "Not Supported Yet"
    update.effective_chat.send_message(message, parse_mode=ParseMode.HTML)
