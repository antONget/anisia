from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def bay_product():
    button1 = InlineKeyboardButton(
        text='ДА! Где прочитать описание курса?',
        url='https://getcourse.ru/'
    )
    button2 = InlineKeyboardButton(
        text='ДА! Куда платить?',
        url='https://getcourse.ru/'
    )
    button3 = InlineKeyboardButton(
        text='Хочу, но не могу ',
        url='https://getcourse.ru/'
    )
    button4 = InlineKeyboardButton(
        text='Не, я и так богиня, у все шикарно',
        url='https://getcourse.ru/'
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button1], [button2], [button3], [button4]]
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


def see_video(cb):
    button = InlineKeyboardButton(
        text='СМОТРИ ВИДЕО',
        callback_data=cb
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button]]
    )
    return keyboard
