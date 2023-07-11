from aiogram import Router
from aiogram.types import Message
from bot.utils.message import remains_answer, submissions_answer, aval_stock_answer


router = Router()


@router.message()
async def echo(message: Message):
    val = message.text.title()
    await remains_answer.remains_answer_summary(message, val)
    await remains_answer.remains_answer_series(message, val)
    await submissions_answer.submissions_answer(message, val)
    await aval_stock_answer.avail_stock_answer(message, val)
