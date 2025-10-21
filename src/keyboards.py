from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def start_reply_kb() -> ReplyKeyboardMarkup:
    kb = [[KeyboardButton(text="Начать игру")]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def options_inline_kb(options: list[str]) -> InlineKeyboardMarkup:
    # callback_data = "answer:<index>"
    buttons = [[InlineKeyboardButton(text=opt, callback_data=f"answer:{i}")]
               for i, opt in enumerate(options)]
    return InlineKeyboardMarkup(inline_keyboard=buttons)