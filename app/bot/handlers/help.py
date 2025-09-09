from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def help_cmd(message: types.Message):
    reply = (
        "<b> 🤖 Personal Productivity Bot – Guide</b>\n\n"
        "<b>📌 Available Commands</b>\n\n"
        "<b>/start</b> – Register yourself\n"
        "<b>/add</b> – Add a new task\n"
        "<b>/tasks</b> – View all tasks\n"
        "<b>/done</b> – Mark a task as completed\n"
        "<b>/clear</b> – Clear all completed tasks\n"
        "<b>/delete</b> – Delete a specific task\n"
        "<b>/help</b> – Show this help message\n"
        "<b> Note: One step at a time and keep being consistent</b>"
    )
    await message.answer(reply, parse_mode="HTML")
