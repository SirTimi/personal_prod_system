from aiogram import Router, types
from aiogram.filters import Command
from sqlmodel import select
from app.db.session import engine, Session
from app.db.models import User
from datetime import datetime

router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    tg_id = message.from_user.id

    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_chat_id == tg_id)).first()

        if not user:
            # Register new user
            user = User(telegram_chat_id=tg_id, created_at=datetime.utcnow())
            session.add(user)
            session.commit()
            session.refresh(user)

    guide = (
        "👋 Welcome to *Your Productivity Bot*!\n\n"
        "Here’s what you can do:\n\n"
        "➕ `/add` – Add a new task\n"
        "📋 `/tasks` – View your task list\n"
        "✅ `/done <task_number>` – Mark a task as completed\n"
        "🧹 `/clear` – Clear all completed tasks\n"
        "📦 `/archived` – View archived tasks\n"
        "ℹ️ `/help` – Show this guide again\n\n"
        "✨ Stay consistent. Productivity compounds."
    )

    await message.answer(guide, parse_mode="Markdown")
