from aiogram import Router, types
from aiogram.filters import Command
from sqlmodel import select
from app.db.session import engine, Session
from app.db.models import User, Task
from datetime import datetime

router = Router()

@router.message(Command("done"))
async def mark_done(message: types.Message):
    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.answer("❌ Usage: /done <task_number>")
        return

    try:
        task_number = int(parts[1])  # per-user task number
    except ValueError:
        await message.answer("⚠️ Task number must be a valid integer.")
        return

    tg_id = message.from_user.id

    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_chat_id == tg_id)).first()
        if not user:
            await message.answer("❌ You’re not registered. Use /start first.")
            return

        task = session.exec(
            select(Task).where(Task.user_id == user.id, Task.task_number == task_number)
        ).first()

        if not task:
            await message.answer(f"⚠️ Task {task_number} not found.")
            return

        task.status = "done"
        task.completed_at = datetime.utcnow()
        session.add(task)
        session.commit()

        await message.answer(f"✅ Task {task_number} marked as done!")
