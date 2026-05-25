import asyncio

from aiogram import Bot, Dispatcher

from app import config
from app.bots.bot_admin.handlers import auth, booking, expenses, keybox_code, messages, report, start


def build_admin_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.include_router(start.router)
    dp.include_router(report.router)
    dp.include_router(booking.router)
    dp.include_router(keybox_code.router)
    dp.include_router(auth.router)
    dp.include_router(expenses.router)
    dp.include_router(messages.router)
    return dp


async def run_admin_bot():
    if not config.ADMIN_BOT_TOKEN:
        print("ADMIN_BOT_TOKEN is not set; admin bot is skipped")
        return

    bot = Bot(token=config.ADMIN_BOT_TOKEN)
    dp = build_admin_dispatcher()
    print("Admin bot started")
    await dp.start_polling(bot)


async def run_client_bot():
    if not config.CLIENT_BOT_TOKEN:
        print("CLIENT_BOT_TOKEN is not set; client bot is skipped")
        return

    from app.bots.bot_clients.bot import bot, dp

    print("Client bot started")
    await dp.start_polling(bot)


async def main():
    tasks = []
    if config.ADMIN_BOT_TOKEN:
        tasks.append(run_admin_bot())
    if config.CLIENT_BOT_TOKEN:
        tasks.append(run_client_bot())

    if not tasks:
        raise RuntimeError("Set ADMIN_BOT_TOKEN and/or CLIENT_BOT_TOKEN")

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
