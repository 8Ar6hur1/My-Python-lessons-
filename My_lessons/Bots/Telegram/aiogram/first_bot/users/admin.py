from aiogram import Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message

admin_route = Router()

@admin_route.message(Command('start'))
async def send_start(message: Message) -> None:
    await message.answer(f'Hello admin, {message.from_user.first_name}!')


@admin_route.message(Command('help'))
async def send_help(message: Message) -> None:
    await message.answer(f'*admin* commands are available:\n1.\n2.\n3.\n4.', parse_mode='Markdown')
