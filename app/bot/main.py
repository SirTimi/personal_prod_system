import asyncio
from aiogram import Bot, Dispatcher
from app.config import settings
from app.bot.handlers import start, tasks, add, done, clear, help
from app.db.session import init_db
import sys

async def main():

     # create tables on startup (safe for Postgres/SQLite)
    print("Initializing DB...")
    init_db()
    print("DB initialized.")
    
    #fail fast if token missing
    if not settings.BOT_TOKEN:
        print("ERROR: BOT_TOKEN environment variable is not set. Exiting.", file=sys.stderr)
        sys.exit(1)

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    # Register handlers
    dp.include_router(start.router)
    dp.include_router(tasks.router)
    dp.include_router(add.router)
    dp.include_router(done.router)
    dp.include_router(clear.router)
    dp.include_router(help.router)

    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
