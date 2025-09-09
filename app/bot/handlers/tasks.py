from aiogram import Router, types
from aiogram.filters import Command
from sqlmodel import select
from app.db.session import engine, Session
from app.db.models import User, Task

router = Router()

@router.message(Command("tasks"))
async def list_tasks(message: types.Message):
    tg_id = message.from_user.id
    parts = message.text.strip().split()

    show_all = len(parts) > 1 and parts[1].lower() == "all"

    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_chat_id == tg_id)).first()
        if not user:
            await message.answer("❌ You’re not registered. Use /start first.")
            return

        query = select(Task).where(Task.user_id == user.id).order_by(Task.created_at)
        if not show_all:
            query = query.where(Task.status == "pending")

        tasks = session.exec(query).all()

        if not tasks:
            await message.answer(
                "🎉 No tasks yet. Add one with /add"
                if not show_all else "📭 No tasks found."
            )
            return

        reply = "📌 *Your Tasks:*\n\n"
        for task in tasks:
            status_icon = "✅" if task.status == "done" else "🟡" if task.status == "pending" else "📦"
            reply += f"[{task.task_number}] {task.title} ({task.priority}) {status_icon}\n"

        await message.answer(reply, parse_mode="Markdown")
