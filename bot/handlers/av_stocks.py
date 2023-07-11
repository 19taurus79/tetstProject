from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from bot.utils.message.aval_stock_answer import avail_stock_answer

router = Router()


@router.message(Command("avail_stock"))
async def av_stock(message: Message, command: CommandObject):
    argument = command.args.title()
    await avail_stock_answer(message, argument)
