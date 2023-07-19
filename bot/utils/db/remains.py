from typing import List
from piccolo.query import Sum
from project_test.tables import Remains


async def get_remains_series(val) -> List:
    ans = await Remains.select(
        Remains.product.product,
        Remains.nomenclature_series,
        Remains.buh,
        Remains.skl,
    ).where(
        (Remains.line_of_business != "Загальні витрати/доходи")
        & (Remains.product.product.ilike(f"%{val}%"))
        & (Remains.buh > 0)
        & (Remains.warehouse == 'Харківський підрозділ  ТОВ "Фірма Ерідон" с.Коротич')
    )

    return ans


async def get_summary_remains(val) -> List:
    summary_buh = (
        await Remains.select(
            Remains.product.product,
            Sum(Remains.buh).as_alias("buh"),
            Sum(Remains.skl).as_alias("skl"),
        )
        .where(
            (Remains.line_of_business != "Загальні витрати/доходи")
            & (Remains.product.product.ilike(f"%{val}%"))
            & (Remains.buh > 0)
            & (
                Remains.warehouse
                == 'Харківський підрозділ  ТОВ "Фірма Ерідон" с.Коротич'
            ),
        )
        .group_by(Remains.product.product)
    )
    return summary_buh
