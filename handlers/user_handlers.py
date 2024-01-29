from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, FSInputFile
from lexicon.lexicon_ru import MESSAGE_TEXT
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.types import CallbackQuery
from resources.video_links import LINK_VIDEO, ID_VIDEO
import pprint
from module.database import add_id, update_name, update_email, update_phone, update_inside, select_row
import asyncio
from aiogram import Bot
import logging
from keyboards.keyboard import bay_product, link_blog, get_contact, see_video
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config_data.config import Config, load_config


router = Router()
# Загружаем конфиг в переменную config
config: Config = load_config()


# состояния бота
class Form(StatesGroup):
    name = State()
    email = State()
    phone = State()
    video0 = State()
    video1 = State()
    video2 = State()
    video3 = State()
    inside = State()
    finish = State()


# Создаем "базу данных" пользователей
user_dict = {}
minutes = 2


@router.message(F.video)
async def process_start_command(message: Message) -> None:
    print(message.video.file_id)
    print(message.video.file_name)


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
    await message.answer(text=MESSAGE_TEXT['email'])
    await state.set_state(Form.email)


@router.message(StateFilter(Form.email))
async def send_video_content(message: Message, state: FSMContext) -> None:
    update_email(message)
    await message.answer(text=MESSAGE_TEXT['phone'],
                         reply_markup=get_contact())
    await state.set_state(Form.phone)


@router.message(StateFilter(Form.phone))
async def send_video_content0(message: Message, state: FSMContext) -> None:
    logging.info(f'send_video_content0: {message.chat.id}')
    update_phone(message)
    keyboard = see_video('video0')
    await message.answer(text=f"{MESSAGE_TEXT['video0']}",
                         reply_markup=keyboard)


@router.callback_query(F.data == 'video0', StateFilter(Form.phone))
async def process_buttons_press_video0(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.video0)
    # await callback.message.answer(text=f"{LINK_VIDEO['video0']}{LINK_VIDEO['video0']}")
    video_id = ID_VIDEO['video0']
    await callback.message.answer_video(video=video_id)
    await asyncio.sleep(2 * minutes)
    keyboard = see_video('video1')
    await callback.message.answer(text=f"{MESSAGE_TEXT['video1']}",
                                  reply_markup=keyboard)


@router.callback_query(F.data == 'video1', StateFilter(Form.video0))
async def process_buttons_press_video1(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.video1)
    video_id = ID_VIDEO['video1']
    await callback.message.answer_video(video=video_id)
    await asyncio.sleep(12 * minutes)
    keyboard = see_video('video2')
    await callback.message.answer(text=f"{MESSAGE_TEXT['video2']}",
                                  reply_markup=keyboard)


@router.callback_query(F.data == 'video2', StateFilter(Form.video1))
async def process_buttons_press_video2(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.video2)
    video_id = ID_VIDEO['video2']
    await callback.message.answer_video(video=video_id)
    await asyncio.sleep(15 * minutes)
    await callback.message.answer(text=MESSAGE_TEXT['inside0'])
    await asyncio.sleep(5)
    await callback.message.answer(text=MESSAGE_TEXT['inside1'])
    await state.set_state(Form.inside)
    await asyncio.sleep(60 * 1 * minutes)  # 24
    scheduler = AsyncIOScheduler()
    # scheduler.add_job(check_state, 'interval', seconds=60, args=('inside', callback.message, state, scheduler))
    scheduler.add_job(check_state, 'cron', hour='10', minute='01', args=('inside', callback.message, state))
    scheduler.start()


@router.message(StateFilter(Form.inside))
async def send_video_content(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.set_state(Form.finish)
    update_inside(message)
    keyboard = see_video('video3')
    await message.answer(f"{MESSAGE_TEXT['video3']}",
                         reply_markup=keyboard)
    await asyncio.sleep(15 * minutes)
    ID, username, name, email, phone, inside = select_row(message)
    await bot.send_message(chat_id=config.tg_bot.admin_ids,
                           text=f'<b>{ID} {username}</b>\n\n'
                                f'<u>Пользователь {name}</u>\n'
                                f'<i>Номер телефона:</i> {phone}\n'
                                f'<i>Email:</i> {email}'
                                f'<i>Инсайд:</i> {inside}')



@router.callback_query(F.data == 'video3', StateFilter(Form.finish))
async def process_buttons_press_video1(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.video3)
    video_id = ID_VIDEO['video3']
    await callback.message.answer_video(video=video_id)
    await asyncio.sleep(3 * minutes)
    await callback.message.answer(text=MESSAGE_TEXT['bay'],
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


