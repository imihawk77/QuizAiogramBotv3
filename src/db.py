import aiosqlite
from typing import Optional, List, Tuple
from datetime import datetime

DB_NAME = "quiz_bot.db"

async def create_tables():
    async with aiosqlite.connect(DB_NAME) as db:
        # Текущее состояние прохождения
        await db.execute("""
        CREATE TABLE IF NOT EXISTS quiz_state (
            user_id INTEGER PRIMARY KEY,
            question_index INTEGER NOT NULL DEFAULT 0,
            correct_count INTEGER NOT NULL DEFAULT 0
        )
        """)
        # Результаты попыток (храним последнюю, но можно копить историю)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS results (
            user_id INTEGER NOT NULL,
            correct INTEGER NOT NULL,
            total INTEGER NOT NULL,
            ts TEXT NOT NULL
        )
        """)
        await db.commit()

# ------ состояние текущего квиза ------
async def get_quiz_index(user_id: int) -> int:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT question_index FROM quiz_state WHERE user_id=?", (user_id,)) as cur:
            row = await cur.fetchone()
            return row[0] if row else 0

async def get_correct_count(user_id: int) -> int:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT correct_count FROM quiz_state WHERE user_id=?", (user_id,)) as cur:
            row = await cur.fetchone()
            return row[0] if row else 0

async def set_quiz_state(user_id: int, question_index: int, correct_count: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO quiz_state (user_id, question_index, correct_count)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET question_index=excluded.question_index, correct_count=excluded.correct_count
        """, (user_id, question_index, correct_count))
        await db.commit()

async def reset_quiz_state(user_id: int):
    await set_quiz_state(user_id, 0, 0)

# ------ результаты ------
async def save_result(user_id: int, correct: int, total: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT INTO results (user_id, correct, total, ts) VALUES (?, ?, ?, ?)",
                         (user_id, correct, total, datetime.utcnow().isoformat()))
        await db.commit()

async def get_user_last_result(user_id: int) -> Optional[Tuple[int, int, str]]:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""
            SELECT correct, total, ts
            FROM results
            WHERE user_id=?
            ORDER BY ts DESC
            LIMIT 1
        """, (user_id,)) as cur:
            row = await cur.fetchone()
            if row:
                return int(row[0]), int(row[1]), row[2]
            return None

async def get_leaderboard(limit: int = 10) -> List[Tuple[int, int, int, str]]:
    """
    Возвращает ТОП по последним результатам каждого игрока:
    (user_id, correct, total, ts)
    """
    async with aiosqlite.connect(DB_NAME) as db:
        # Берём последнюю запись каждого пользователя
        query = """
        WITH last_res AS (
            SELECT r.user_id, r.correct, r.total, r.ts
            FROM results r
            JOIN (
                SELECT user_id, MAX(ts) AS max_ts
                FROM results
                GROUP BY user_id
            ) l ON r.user_id = l.user_id AND r.ts = l.max_ts
        )
        SELECT user_id, correct, total, ts
        FROM last_res
        ORDER BY correct DESC, ts DESC
        LIMIT ?
        """
        async with db.execute(query, (limit,)) as cur:
            rows = await cur.fetchall()
            return [(int(r[0]), int(r[1]), int(r[2]), r[3]) for r in rows]