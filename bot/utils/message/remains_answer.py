from bot.utils.db.remains import get_remains_series, get_summary_remains
from bot.utils.db.submissions import quantity_under_orders
from aiogram.exceptions import TelegramBadRequest as err


async def remains_answer_series(message, val):
    await message.answer(f"<b>*****Отатки с партиями*****</b>{chr(10)}{chr(10)}")
    ans = await get_remains_series(val)
    under_orders = await quantity_under_orders(val)
    a = []
    if len(ans) > 0:
        for i in range(len(ans)):
            if i == 0:
                a.append(
                    f"<strong><u>{ans[i].get('product')}</u></strong>{chr(10)}"
                    f"Партия {ans[i].get('nomenclature_series')} по бухгалтерии {ans[i].get('buh')} по складу {ans[i].get('skl')}{chr(10)}"
                )
            if i > 0:
                if ans[i - 1].get("product") != ans[i].get("product"):
                    a.append(
                        f"<strong><u>{ans[i].get('product')}</u></strong>{chr(10)}"
                        f"Партия {ans[i].get('nomenclature_series')} по бухгалтерии {ans[i].get('buh')} по складу {ans[i].get('skl')}{chr(10)}"
                    )
                if ans[i - 1].get("product") == ans[i].get("product"):
                    a.append(
                        f"Партия {ans[i].get('nomenclature_series')} по бухгалтерии {ans[i].get('buh')} по складу {ans[i].get('skl')}{chr(10)}"
                    )
        try:
            await message.answer("".join(a))
        except err:
            await message.answer(
                f"Вероятно слишком длинное сообщение{chr(10)}"
                f"Попробуйте конкретизировать данные для поиска"
            )
    if len(ans) == 0:
        await message.answer("Остатков нет")


async def remains_answer_summary(message, val):
    await message.answer(f"<b>*****Отатки*****</b>{chr(10)}{chr(10)}")
    ans = await get_summary_remains(val)
    a = []
    if len(ans) > 0:
        for i in range(len(ans)):
            a.append(
                f"<strong><u>{ans[i].get('product')}{chr(10)}"
                f"Бухгалтерия {ans[i].get('buh')} Склад {ans[i].get('skl')}</u></strong>{chr(10)}{chr(10)}"
            )
        await message.answer("".join(a))
    if len(ans) == 0:
        await message.answer("Остатков нет")
