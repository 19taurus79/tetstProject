from fastapi import FastAPI
from bot.project_test.tables import Agent, Client
from typing import Optional

app = FastAPI(title="ProjectTest")


@app.get("/")
async def read_root():
    """Тестовая функция"""
    return {"Hello": "world"}


@app.post("/agent")
async def add_agent(name: str):
    """Функция добавления агента в БД"""
    await Agent.insert(Agent(name=name))


@app.get("/agent")
async def get_agent(name: Optional[str] = None):
    """Функция получения агента из БД. Если данные не передаются,
    возвращаяюся все"""
    qwery = Agent.objects()
    if name:
        qwery = qwery.where(Agent.name == name)
    result = await qwery
    return result


@app.post("/client")
async def post_client(name: str, agent: str):
    await Client.insert(Client(name=name, agent=agent))


@app.get("/client")
async def get_client(name: Optional[str] = None):
    qwery = Client.objects()
    if name:
        qwery = qwery.where(Client.name == name)
    result = await qwery
    return result


@app.get("/client-agent")
async def get_client_agent(name: str):
    qwery = Client.select(Client.name, Client.agent.all_columns()).where(
        Client.name == name
    )
    result = await qwery
    return result
