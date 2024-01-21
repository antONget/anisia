from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message
from lexicon.lexicon_ru import MESSAGE_TEXT
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.types import CallbackQuery
from resources.video_links import LINK_VIDEO

from module.database import add_id, update_name, update_phone, update_inside, select_row
import asyncio
from aiogram import Bot
import logging
from keyboards.keyboard import bay_product, link_blog, get_contact
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config_data.config import Config, load_config


router = Router()
# Загружаем конфиг в переменную config
config: Config = load_config()


# состояния бота
class Form(StatesGroup):
    name = State()
    phone = State()
    inside = State()
    finish = State()


# Создаем "базу данных" пользователей
user_dict = {}
minutes = 2


# Этот handler срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext, bot: Bot) -> None:
    logging.info(f'process_start_command: {message.chat.id}')
    add_id(message)
    if message.from_user.first_name is None:
        await bot.send_message(chat_id=config.tg_bot.admin_ids,
                               text=f'{message.chat.id} - '
                                    f'Пользователь {message.from_user.first_name} '
                                    f'зашел в воронку')
    else:
        await bot.send_message(chat_id=config.tg_bot.admin_ids,
                               text=f'{message.chat.id} - '
                                    f'Пользователь зашел в воронку')
    await message.answer(text=MESSAGE_TEXT['greet'])
    await asyncio.sleep(2)
    await message.answer(text=MESSAGE_TEXT['name'])
    await state.set_state(Form.name)


@router.message(StateFilter(Form.name))
async def send_video_content(message: Message, state: FSMContext) -> None:
    update_name(message)
    await message.answer(text=MESSAGE_TEXT['phone'],
                         reply_markup=get_contact())
    await state.set_state(Form.phone)


@router.message(StateFilter(Form.phone))
async def send_video_content(message: Message, state: FSMContext) -> None:
    update_phone(message)
    await message.answer(f"{LINK_VIDEO['video1']}{LINK_VIDEO['video1']}")
    await asyncio.sleep(3 * minutes)
    await message.answer(f"{LINK_VIDEO['video2']}{LINK_VIDEO['video2']}")
    await asyncio.sleep(3 * minutes)
    await message.answer(text=MESSAGE_TEXT['inside1'])
    await state.set_state(Form.inside)
    await asyncio.sleep(60 * 1 * minutes)  # 24
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_state, 'interval', seconds=60, args=('inside', message, state, scheduler))
    # scheduler.add_job(check_state, 'cron', hour='10', minute='01', args=('inside', message, state))
    scheduler.start()


@router.message(StateFilter(Form.inside))
async def send_video_content(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.set_state(Form.finish)
    update_inside(message)
    await message.answer(f"{LINK_VIDEO['video3']}{LINK_VIDEO['video3']}")
    await asyncio.sleep(3 * minutes)
    ID, username, name, phone, inside = select_row(message)
    await bot.send_message(chat_id=config.tg_bot.admin_ids,
                           text=f'<b>{ID} {username}</b>\n\n'
                                f'<u>Пользователь {name}</u>\n'
                                f'<i>Номер телефона:</i> {phone}\n'
                                f'<i>Инсайд:</i> {inside}')
    await message.answer(text=MESSAGE_TEXT['bay'],
                         reply_markup=bay_product())


async def check_state(chek_state: str, message: Message, state: FSMContext, scheduler):
    current_state = await state.get_state()  # текущее машинное состояние пользователя
    if current_state == f'Form:{chek_state}':
        logging.info(f'check1_state-{chek_state}: {message.chat.id}')
        await message.answer(text=MESSAGE_TEXT['inside2'])
        await asyncio.sleep(60 * 1 * minutes)  # 24
        current_state = await state.get_state()
        if current_state == f'Form:{chek_state}':
            logging.info(f'check2_state-{chek_state}: {message.chat.id}')
            await message.answer(text=MESSAGE_TEXT['inside3'],
                                 reply_markup=link_blog())
    scheduler.shutdown()


