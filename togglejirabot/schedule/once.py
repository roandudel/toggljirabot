from telegram import ParseMode
from telegram.ext import CallbackContext

from togglejirabot.settings import TELEGRAM_CHAT_ID


def once(context: CallbackContext):
    message = "GER-15 Sachen aufgeräumt: 15.25h \r\n" \
              "GER-16 Noch aufgeräumt: 2.25h".replace('-', '\\-').replace('.', '\\-')

    context.bot.send_message(chat_id=TELEGRAM_CHAT_ID,
                             parse_mode=ParseMode.MARKDOWN_V2,
                             text=message)
