from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def weekly_keyboard_markup():
    keyboard = [
        [
            InlineKeyboardButton("Last Week", callback_data='last'),
            InlineKeyboardButton("This Week", callback_data='this'), ]
    ]

    return InlineKeyboardMarkup(keyboard)
