from uagents import Agent, Context, Model
from fastapi import FastAPI

# Создание агента с именем "all_features_agent"
agent = Agent(name="all_features_agent", seed="all_features_agent_seed", endpoint="127.0.0.1", port="8001")

# Пример модели сообщения
class CustomMessage(Model):
    text: str

class ResponseMessage(Model):
    response: str
    
# Создание FastAPI приложения
app = FastAPI()

# Обработка GET-запроса на корневой URL
@app.get("/")
async def read_root():
    return {"message": "Агент работает"}

# Интеграция FastAPI приложения с агентом
# agent.include_router(app)


# Обработка события запуска
@agent.on_event("startup")
async def on_startup(ctx: Context):
    ctx.logger.info("Агент запущен")
    ctx.storage.set("startup_count", 0)
    # Отправка сообщения самому агенту для имитации пользовательского события
    await ctx.send(ctx.agent.address, CustomMessage(text="Тригерное событие при запуске"))

# Обработка события завершения работы
@agent.on_event("shutdown")
async def on_shutdown(ctx: Context):
    ctx.logger.info("Агент остановлен")

# Обработка пользовательского события
@agent.on_message(model=CustomMessage)
async def on_custom_event(ctx: Context, sender: str, message: CustomMessage):
    ctx.logger.info(f"Произошло пользовательское событие с сообщением: {message.text}")

# Обработка сообщения
@agent.on_message(model=CustomMessage)
async def handle_message(ctx: Context, sender: str, message: CustomMessage):
    ctx.logger.info(f'Полученное сообщение: {message.text}')
    await ctx.send(sender, ResponseMessage(response="Сообщение получено."))

# Обработка интервала
@agent.on_interval(period=15.0)
async def on_interval(ctx: Context):
    startup_count = ctx.storage.get("startup_count")
    if startup_count is None:
        startup_count = 0
    ctx.logger.info(f"Agent has started {startup_count} times.")
    ctx.storage.set("startup_count", startup_count + 1)

# Обработка запросов
@agent.on_query(model=CustomMessage, replies={ResponseMessage})
async def query_handler(ctx: Context, sender: str, query: CustomMessage):
    ctx.logger.info(f"Получен запрос: {query.text}")
    await ctx.send(sender, ResponseMessage(response="Запрос обработан"))

if __name__ == "__main__":
    agent.run()
