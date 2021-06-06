from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from togglejirabot.decorators import security


@security
def command_emoji(update: Update, context: CallbackContext):
    # message = '[Google](http://google.de)'D
    message = """<b>Я — твой личный бот для Вастрик.Клуба</b>"""

    context.bot.send_message(chat_id=update.effective_chat.id,
                             parse_mode=ParseMode.HTML,
                             text=message)
