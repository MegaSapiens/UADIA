from uagents import Agent, Context, Model

# Создание агента с именем "all_features_agent"
agent = Agent(name="all_features_agent", seed="all_features_agent_seed")

# Пример модели сообщения
class CustomMessage(Model):
    text: str

class ResponseMessage(Model):
    response: str

# Обработка события запуска
@agent.on_event("startup")
async def on_startup(ctx: Context):
    ctx.logger.info("Agent is starting up")
    ctx.storage.set("startup_count", 0)
    # Отправка сообщения самому агенту для имитации пользовательского события
    await ctx.send(ctx.agent.address, CustomMessage(text="Triggering custom event"))

# Обработка события завершения работы
@agent.on_event("shutdown")
async def on_shutdown(ctx: Context):
    ctx.logger.info("Agent is shutting down")

# Обработка пользовательского события
@agent.on_message(model=CustomMessage)
async def on_custom_event(ctx: Context, sender: str, message: CustomMessage):
    ctx.logger.info(f"Custom event occurred with message: {message.text}")

# Обработка сообщения
@agent.on_message(model=CustomMessage)
async def handle_message(ctx: Context, sender: str, message: CustomMessage):
    ctx.logger.info(f'Received message: {message.text}')
    await ctx.send(sender, ResponseMessage(response="Message received"))

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
    ctx.logger.info(f"Query received: {query.text}")
    await ctx.send(sender, ResponseMessage(response="Query processed"))

if __name__ == "__main__":
    agent.run()
