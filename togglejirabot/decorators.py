from telegram import Update
from telegram.ext import CallbackContext

from togglejirabot.settings import TELEGRAM_CHAT_ID


def security(callback):
    def wrapper(update: Update, context: CallbackContext):
        user = update.effective_user
        if update.effective_chat.id != TELEGRAM_CHAT_ID:
            print(f"Someone tried to use your bot. It is: {user['first_name']} {user['last_name']} {update.effective_chat.id}")
            return None

        return callback(update, context)

    return wrapper
