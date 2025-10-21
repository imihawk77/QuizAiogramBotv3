from aiogram import Router, types
from aiogram.filters import Command
from src.keyboards import start_reply_kb
from src.db import get_user_last_result, get_leaderboard

common_router = Router()

@common_router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Добро пожаловать в квиз! Нажми «Начать игру» или используй /quiz",
        reply_markup=start_reply_kb()
    )

@common_router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    user_id = message.from_user.id
    # личный последний результат
    last = await get_user_last_result(user_id)
    if last:
        correct, total, ts = last
        you = f"Твой последний результат: {correct}/{total} (UTC {ts})"
    else:
        you = "Пока нет результатов. Сыграй /quiz"

    # лидерборд по последним результатам
    board = await get_leaderboard(limit=10)
    if board:
        lines = []
        for idx, (uid, c, t, ts) in enumerate(board, start=1):
            tag = "- это ты" if uid == user_id else ""
            lines.append(f"{idx}. {uid}: {c}/{t} (UTC {ts}) {tag}")
        top = "\n".join(lines)
        await message.answer(f"{you}\n\n ТОП последних результатов:\n{top}")
    else:
        await message.answer(you)