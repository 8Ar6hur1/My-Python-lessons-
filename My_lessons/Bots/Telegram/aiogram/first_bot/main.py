# logging
import logging

# aiogram
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.filters import CommandStart, Command

# asyncio
import asyncio

# os
import os

# dotenv
from dotenv import load_dotenv

# project: admin, user
from users import admin, user
from users.admin import admin_route, send_help as admin_send_help
from users.user import user_route, send_help as user_send_help


logging.basicConfig(level=logging.INFO)

load_dotenv()

# API токен телеграм боту
API_TOKEN = os.getenv('API_TOKEN')

# Перевіряємо чи є у нас файл .env 
if API_TOKEN is None:
    raise ValueError('API_TOKEN is not set in the environment or .env file')

admin_ids_str = os.getenv('ADMIN_IDS', '')

# Переконуємось, що ADMIN_IDS коректно завантажено
if admin_ids_str:
    # завантажуємо ADMIN_IDS з файлу .env і перетворюємо його на список цілих чисел.
    ADMIN_IDS = list(map(int, os.getenv('ADMIN_IDS').split(',')))
else:
    ADMIN_IDS = []

# Перевірка чи правильно завантажується ADMIN_IDS з .env
print(f'Loaded ADMIN_IDS: {ADMIN_IDS}')


bot = Bot(token=API_TOKEN)
dp = Dispatcher()

dp.include_router(admin_route)
dp.include_router(user_route)


# перевіряємо, чи є user_id в списку адміністраторів, який зберігається в ADMIN_IDS
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@dp.message(CommandStart())
async def start_bot(message: Message):

    r_markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Site'), KeyboardButton(text='Welcome')],
        ],
        resize_keyboard=True
    )

    await message.answer('Choose an option:', reply_markup=r_markup)

# перевіряємо яке повідомлення кидати користувачу на команду 'start'
    user_id = message.from_user.id
    if is_admin(user_id):
        await admin.send_start(message)
    else:
        await user.send_start(message)

    # Створення инлайн-клавіатури
    i_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Site', url='https://aiogram.dev')],
            [InlineKeyboardButton(text='Hello', callback_data='hello')],
            [InlineKeyboardButton(text='Welcome', callback_data='welcome')]
        ]
    )
    await message.answer("Please choose an option:", reply_markup=i_markup)


@dp.callback_query(lambda c: c.data)
async def process_callback(callback_query: CallbackQuery):
    if callback_query.data == 'welcome':
        await bot.answer_callback_query(callback_query.id, 'Option "welcom" selected!')
    elif callback_query.data == 'hello':
        await bot.answer_callback_query(callback_query.id, 'Option "hello" selected!')


# перевіряємо яке повідомлення кидати користувачу на команду 'help'
@dp.message(Command('help'))
async def send_help(message: Message):
    user_id = message.from_user.id
    if is_admin(user_id):
        await admin_send_help(message)
    else:
        await user_send_help(message)


async def main():
    print('Starting bot...')
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
