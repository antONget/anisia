from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def bay_product():
    button = InlineKeyboardButton(
        text='КУПИТЬ ПРОДУКТ',
        url='https://getcourse.ru/'
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button]]
    )
    return keyboard

def link_blog():
    button = InlineKeyboardButton(
        text='МОЙ БЛОГ',
        url='https://t.me/nisi_revival'
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button]]
    )
    return keyboard


def get_contact():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=True,
                                   keyboard=[[KeyboardButton(text='Отправить номер телефона',
                                                             request_contact=True)]])
    return keyboard
