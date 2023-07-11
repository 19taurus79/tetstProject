from typing import List

from project_test.tables import AvailableStock


async def get_available_stock(val) -> List:
    aval = await AvailableStock.select(
        AvailableStock.product,
        AvailableStock.buying_season,
        AvailableStock.division,
        AvailableStock.available,
    ).where(
        (AvailableStock.product.ilike(f"%{val}%"))
        & (AvailableStock.available > 0)
        & (AvailableStock.line_of_business != "Загальні витрати/доходи")
    )
    return aval
