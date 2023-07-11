from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from bot.utils.message.submissions_answer import submissions_answer
from aiogram.fsm.state import StatesGroup, State
from bot.handlers.remains import CommandBot
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(Command("submissions"))
async def submissions(message: Message, state: FSMContext):
    await message.answer("Укажите номенклатуру :")
    await state.set_state(CommandBot.choosing_submission)
    # await submissions_answer(message, arguments)
