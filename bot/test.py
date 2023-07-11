import asyncio
from pprint import pprint

from bot.create_bot import conn


async def np(city):
    url = "https://api.novaposhta.ua/v2.0/json/"
    api_key = "f79fe8a8e39639de6678d70cb0c9250c"
    data = {
        "apiKey": api_key,
        "modelName": "Address",
        "calledMethod": "getSettlements",
        "methodProperties": {
            "Page": "1",
            "Warehouse": "1",
            "FindByString": city,
            "Limit": "20",
        },
    }
    conn_2 = await conn
    async with conn_2.get(url, json=data) as response:
        # print(response.status)
        pprint(await response.json())


# if __name__ == "__main__":
#     asyncio.run(np("Харків"))
