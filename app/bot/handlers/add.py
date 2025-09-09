from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlmodel import select
from app.db.session import engine, Session
from app.db.models import User
from app.services.task_service import create_task

router = Router()

# Define FSM states
class AddTask(StatesGroup):
    waiting_for_title = State()

@router.message(Command("add"))
async def add_task(message: types.Message, state: FSMContext):
    await message.answer("✍️ What’s the task?")
    await state.set_state(AddTask.waiting_for_title)

@router.message(AddTask.waiting_for_title, F.text)
async def save_task(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    with Session(engine) as session:
        user = session.exec(select(User).where(User.telegram_chat_id == tg_id)).first()
        if not user:
            await message.answer("❌ You’re not registered. Use /start first.")
            return
    
    title = message.text.strip()
    task = create_task(user.id, title)

    await message.answer(f"✅ Task added: {task.title}")
    await state.clear()