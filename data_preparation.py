import pandas as pd
import sqlalchemy
from sqlalchemy import text

from connection import engine


def get_submission():
    submissions_xls = pd.read_excel("Заявки.xlsx", header=None)
    step1 = submissions_xls.drop(submissions_xls.columns[[0, 1, 2, 3, 4, 5]])
    step2 = step1.rename(columns=step1.iloc[0])
    step3 = step2.dropna(axis="columns", how="all")
    step4 = step3.drop(step3.index[[0, 1, 2]], axis=0)
    step5 = step4.drop(step4.tail(1).index, axis=0)
    names = [
        "division",
        "manager",
        "company_group",
        "client",
        "contract_supplement",
        "parent_element",
        "manufacturer",
        "active_ingredient",
        "nomenclature",
        "party_sign",
        "buying_season",
        "line_of_business",
        "period",
        "shipping_warehouse",
        "document_status",
        "delivery_status",
        "shipping_address",
        "transport",
        "plan",
        "fact",
        "different",
    ]
    step5.columns = names
    step5.reset_index(drop=True, inplace=True)
    step5["buying_season"].fillna(" ", inplace=True)
    step5.loc[(step5["party_sign"] == "Закупівля поточного сезону"), "party_sign"] = " "
    step5["product"] = step5.apply(
        lambda row: str(row["nomenclature"])
        + " "
        + str(row["party_sign"])
        + " "
        + str(row["buying_season"]),
        axis=1,
    )
    step5["fact"].fillna(0, inplace=True)
    step5["different"].fillna(0, inplace=True)
    step5["plan"].fillna(0, inplace=True)
    step5.to_excel("submissions.xlsx")
    data_type = {
        "plan": sqlalchemy.types.BIGINT,
        "fact": sqlalchemy.types.BIGINT,
        "different": sqlalchemy.types.BIGINT,
    }
    step5.to_sql(
        con=engine,
        if_exists="replace",
        name="submissions_tmp",
        index=False,
        dtype=data_type,
    )
    clean_table_sql = """
                   TRUNCATE submissions
                   """
    update_sql = """
                   INSERT INTO submissions(division,manager,company_group,client,contract_supplement,parent_element,
                   manufacturer,active_ingredient,nomenclature,party_sign,buying_season,line_of_business,period,
                   shipping_warehouse,document_status,delivery_status,shipping_address,transport,plan,fact,different,product)
                   SELECT division,manager,company_group,client,contract_supplement,parent_element,
                   manufacturer,active_ingredient,nomenclature,party_sign,buying_season,line_of_business,period,
                   shipping_warehouse,document_status,delivery_status,shipping_address,transport,plan,fact,different,product
                    FROM submissions_tmp
                   """
    with engine.connect() as conn:
        conn.execute(text(clean_table_sql))
        conn.execute(text(update_sql))
        conn.commit()
    return print("Файл с заявками обработан")


def product_guide():
    data = pd.read_excel("submissions.xlsx")
    product = data[["product", "line_of_business"]]
    product.drop_duplicates(
        subset=["product", "line_of_business"], keep="first", inplace=True
    )
    product.reset_index(drop=True, inplace=True)
    product.to_sql(
        con=engine, if_exists="replace", name="product_guide_temp", index=False
    )
    clean_table_sql = """
    TRUNCATE product_guide
    """
    update_sql = """
    INSERT INTO product_guide(product, line_of_business)
    SELECT product, line_of_business FROM product_guide_temp
    """
    with engine.connect() as conn:
        conn.execute(text(clean_table_sql))
        conn.execute(text(update_sql))
        conn.commit()
    product.to_excel("product.xlsx")
    return print("Справочник товаров получен")


def client_guide():
    data = pd.read_excel("submissions.xlsx")
    client = data[["client", "company_group"]]
    client.drop_duplicates(
        subset=["client", "company_group"], keep="first", inplace=True
    )
    client.reset_index(drop=True, inplace=True)
    client.to_sql(con=engine, if_exists="replace", name="client_guide_tmp", index=False)
    client.to_excel("client.xlsx")
    clean_table_sql = """
        TRUNCATE client_guide
        """
    update_sql = """
        INSERT INTO client_guide(client, company_group)
        SELECT client, company_group FROM client_guide_tmp
        """
    with engine.connect() as conn:
        conn.execute(text(clean_table_sql))
        conn.execute(text(update_sql))
        conn.commit()
    return print("Справочник клиентов получен")


def manager_guide():
    data = pd.read_excel("submissions.xlsx")
    manager = data["manager"]
    manager.drop_duplicates(keep="first", inplace=True)
    manager.reset_index(drop=True, inplace=True)
    manager.to_sql(
        con=engine, if_exists="replace", name="manager_guide_tmp", index=False
    )
    manager.to_excel("manager.xlsx")
    clean_table_sql = """
            TRUNCATE manager_guide
            """
    update_sql = """
            INSERT INTO manager_guide(manager)
            SELECT manager FROM manager_guide_tmp
            """
    with engine.connect() as conn:
        conn.execute(text(clean_table_sql))
        conn.execute(text(update_sql))
        conn.commit()
    return print("Справочник менеджеров получен")


def get_remains():
    remains_xls = pd.read_excel("Остатки.xlsx", header=None)
    step1 = remains_xls.drop(remains_xls.columns[[0, 1, 2, 4]])
    step2 = step1.rename(columns=step1.iloc[0])
    step3 = step2.dropna(axis="columns", how="all")
    step4 = step3.drop(step3.index[[0, 1]], axis=0)
    step5 = step4.drop(step4.tail(1).index, axis=0)
    step5.columns = [
        "line_of_business",
        "warehouse",
        "parent_element",
        "nomenclature",
        "party_sign",
        "buying_season",
        "nomenclature_series",
        "mtn",
        "origin_country",
        "germination",
        "crop_year",
        "quantity_per_pallet",
        "active_substance",
        "certificate",
        "certificate_start_date",
        "certificate_end_date",
        "buh",
        "skl",
        "weight",
    ]
    step5.reset_index(drop=True, inplace=True)
    step5["buying_season"].fillna(" ", inplace=True)
    step5["party_sign"].fillna(" ", inplace=True)
    step5["product"] = step5.apply(
        lambda row: str(row["nomenclature"])
        + " "
        + str(row["party_sign"])
        + " "
        + str(row["buying_season"]),
        axis=1,
    )
    step5["buh"].fillna(0, inplace=True)
    step5["skl"].fillna(0, inplace=True)
    step5.to_excel("remains.xlsx")
    data_type = {"buh": sqlalchemy.types.BIGINT, "skl": sqlalchemy.types.BIGINT}
    step5.to_sql(
        con=engine,
        if_exists="replace",
        name="remains_tmp",
        index=False,
        dtype=data_type,
    )
    clean_table_sql = """
               TRUNCATE remains
               """
    update_sql = """
               INSERT INTO remains(line_of_business, warehouse, 
               parent_element, nomenclature, party_sign, buying_season,
               nomenclature_series,mtn,origin_country,germination,
               crop_year,quantity_per_pallet,active_substance,certificate,
               certificate_start_date,certificate_end_date,buh,skl,weight,product)
               SELECT line_of_business,warehouse,
               parent_element,nomenclature,party_sign,buying_season,
               nomenclature_series,mtn,origin_country,germination,
               crop_year,quantity_per_pallet,active_substance,certificate,
               certificate_start_date,certificate_end_date,buh,skl,weight,product
                FROM remains_tmp
               """
    with engine.connect() as conn:
        conn.execute(text(clean_table_sql))
        conn.execute(text(update_sql))
        conn.commit()
    return print("Файл с остатками обработан")


def get_available_stock():
    available_stock_xls = pd.read_excel(
        "Доступность товара подразделения.xlsx", header=None
    )
    step1 = available_stock_xls.drop(
        available_stock_xls.columns[[0, 1, 2, 3, 4, 5, 6, 7]]
    )
    step2 = step1.rename(columns=step1.iloc[0])
    step3 = step2.dropna(axis="columns", how="all")
    step4 = step3.drop(step3.index[[1, 4]], axis=0)
    step5 = step4.drop(step4.tail(1).index, axis=0)
    names = [
        "nomenclature",
        "party_sign",
        "buying_season",
        "division",
        "line_of_business",
        "available",
    ]
    step5.columns = names
    step5.reset_index(drop=True, inplace=True)
    step5["buying_season"].fillna(" ", inplace=True)
    step5["party_sign"].fillna(" ", inplace=True)
    step5["product"] = step5.apply(
        lambda row: str(row["nomenclature"])
        + " "
        + str(row["party_sign"])
        + " "
        + str(row["buying_season"]),
        axis=1,
    )
    step5["available"].fillna(0, inplace=True)
    step5.to_excel("available_stock.xlsx")
    data_type = {"available": sqlalchemy.types.BIGINT}
    step5.to_sql(
        con=engine,
        if_exists="replace",
        name="available_stock_tmp",
        index=False,
        dtype=data_type,
    )
    clean_table_sql = """
                       TRUNCATE available_stock
                       """
    update_sql = """
                       INSERT INTO available_stock(nomenclature,party_sign,buying_season,division,
                       line_of_business,available,product)
                       SELECT nomenclature,party_sign,buying_season,division,
                       line_of_business,available,product
                        FROM available_stock_tmp
                       """
    with engine.connect() as conn:
        conn.execute(text(clean_table_sql))
        conn.execute(text(update_sql))
        conn.commit()
    return print("Файл со свободными остатками обработан")


if __name__ == "__main__":
    get_submission()
    # product_guide()
    # client_guide()
    # manager_guide()
    get_remains()
    get_available_stock()
