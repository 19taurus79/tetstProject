from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from bot.keyboards import kb
from aiogram.fsm.context import FSMContext
from bot.utils.message.remains_answer import (
    remains_answer_summary,
    remains_answer_series,
)
from bot.utils.message.submissions_answer import submissions_answer

av_todo = ["без партии", "с партией"]


class CommandBot(StatesGroup):
    choosing_remains_type = State()
    choosing_remains_nomenclature = State()
    choosing_submission = State()
    show_submission = State()


router = Router()


@router.message(Command("remains"))
async def remains(message: Message, state: FSMContext):
    await message.answer(
        "В каком виде показать остатки ?", reply_markup=kb.make_row_keyboard(av_todo)
    )

    await state.set_state(CommandBot.choosing_remains_type)


@router.message(CommandBot.choosing_remains_type, F.text.in_(av_todo))
async def get_remains(message: Message, state: FSMContext):
    await state.update_data(chosen_remains_type=message.text)
    await message.answer("Укажите номенклатуру :", reply_markup=ReplyKeyboardRemove)
    await state.set_state(CommandBot.choosing_remains_nomenclature)


@router.message(CommandBot.choosing_remains_nomenclature)
async def get_nomenclature(message: Message, state: FSMContext):
    await state.update_data(chosen_nomenclature=message.text.capitalize())
    data = await state.get_data()
    remains_type = data.get("chosen_remains_type")
    nomenclature = data.get("chosen_nomenclature")
    if remains_type == "без партии":
        await remains_answer_summary(message, nomenclature)
    if remains_type == "с партией":
        await remains_answer_series(message, nomenclature)
    await message.answer(
        f"{chr(10)}Показать у кого заявки на эту номенклатуру ?",
        reply_markup=kb.make_row_keyboard(["Да", "Нет"]),
    )
    await state.set_state(CommandBot.show_submission)
    # await state.clear()


@router.message(CommandBot.show_submission, F.text.in_(["Да", "Нет"]))
async def show_submission(message: Message, state: FSMContext):
    data = await state.get_data()
    nomenclature = data.get("chosen_nomenclature")
    if message.text == "Да":
        await submissions_answer(message, nomenclature)
    if message.text == "Нет":
        await message.answer("Ok", reply_markup=ReplyKeyboardRemove)
    await state.clear()
