from aiogram import Router, types
from aiogram.filters import Command
from sqlmodel import select, delete
from app.db.session import engine, Session
from app.db.models import User, Task

router = Router()

@router.message(Command("clear"))
async def clear_done_tasks(message: types.Message):
    tg_id = message.from_user.id

    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_chat_id == tg_id)).first()
        if not user:
            await message.answer("❌ You’re not registered. Use /start first.")
            return

        # Count first, then delete
        done_tasks = session.exec(
            select(Task).where(Task.user_id == user.id, Task.status == "done")
        ).all()

        if not done_tasks:
            await message.answer("⚠️ You don’t have any completed tasks to clear.")
            return

        stmt = delete(Task).where(Task.user_id == user.id, Task.status == "done")
        session.exec(stmt)
        session.commit()

        await message.answer(f"🧹 Cleared {len(done_tasks)} completed task(s).")
