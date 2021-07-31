import logging

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

from togglejirabot.decorators import security
from togglejirabot.handlers import booker, daily, emoji, start, weekly
from togglejirabot.settings import TELEGRAM_API_TOKEN


@security
def command_help(update: Update, context: CallbackContext) -> None:
    update.effective_chat.send_message('/start\n'
                                       '/emoji\n'
                                       '/weekly\n'
                                       '/daily\n'
                                       )


def main() -> None:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    updater = Updater(token=TELEGRAM_API_TOKEN)
    dispatcher = updater.dispatcher
    # job_queue = updater.job_queue
    # job_queue.run_repeating(once, interval=60)
    dispatcher.add_handler(CommandHandler('help', command_help))
    dispatcher.add_handler(CommandHandler('start', start.command_start))
    dispatcher.add_handler(CommandHandler('emoji', emoji.command_emoji))
    dispatcher.add_handler(CommandHandler('weekly', weekly.command_weekly))
    dispatcher.add_handler(CommandHandler('daily', daily.command_daily))
    dispatcher.add_handler(CommandHandler('booker', booker.command_booker))
    updater.start_polling()


if __name__ == '__main__':
    main()
