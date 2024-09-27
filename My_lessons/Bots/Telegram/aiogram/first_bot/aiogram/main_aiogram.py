# aiogram
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram import Router

# asyncio
import asyncio

# os
import os

# dotenv
from dotenv import load_dotenv

# project
from admin import admin_route
from user import user_route


load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

if API_TOKEN is None:
    raise ValueError('API_TOKEN is not set in the environment or .env file')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

dp.include_router(admin_route)
dp.include_router(user_route)

@dp.message(CommandStart())
async def command_start_hadler(message: Message):
    await message.answer(f'Hello {message.from_user.first_name}')


@dp.message(Command('help'))
async def send_help(message: Message):
    await message.answer(f'I don\'t Help, {message.from_user.full_name}')




async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
