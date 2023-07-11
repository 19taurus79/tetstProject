from typing import List

from piccolo.query import Sum

from project_test.tables import Submissions


async def get_submissions(val) -> List:
    sub = (
        await Submissions.select(
            Submissions.manager,
            Submissions.client,
            Submissions.different,
            Submissions.product,
        )
        .where(
            (Submissions.line_of_business != "Загальні витрати/доходи")
            & (Submissions.product.ilike(f"%{val}%"))
            & (
                Submissions.shipping_warehouse
                == 'Харківський підрозділ  ТОВ "Фірма Ерідон" с.Коротич'
            )
            & (Submissions.different > 0)
            & (Submissions.document_status == "затверджено")
        )
        .order_by("product")
    )
    return sub


async def quantity_under_orders(nom) -> List:
    under_orders = (
        await Submissions.select(Submissions.product, Sum(Submissions.different))
        .where(
            (Submissions.product.ilike(f"%{nom}%")),
            (Submissions.document_status == "затверджено")
            & (Submissions.different > 0)
            & (
                Submissions.shipping_warehouse
                == 'Харківський підрозділ  ТОВ "Фірма Ерідон" с.Коротич'
            ),
        )
        .group_by(Submissions.product)
    )
    return under_orders
