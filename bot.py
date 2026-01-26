import asyncio
import sqlite3
import time

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ================== SOZLAMALAR ==================
TOKEN = "8379681025:AAG0MgojPZSmHAV7rJbl7_I8M5o04Sz2UA4"
ADMIN_ID = 6140962854
DB_NAME = "votes.db"
VOTING_DURATION = 7 * 24 * 60 * 60  # 7 kun

CHANNELS = ["@azizacademy_uz", "@codingwith_ulugbek"]

SUBJECTS = [
    "English", "Rus", "Koreys", "Arab", "Matematika",
    "Mental", "Pochemuchka", "Hamshiralik",
    "IT", "Kampyuter", "Loyiha"
]

# ================== O‘QUVCHILAR ==================
SPECIAL_STUDENTS = {

    ("English", "junior"): [
        "ALIBOYEVA SADOQAT 5-maktab 7-sinf (Olmazor)",
        "ULUGBEKOV FAYOZBEK 25-maktab 6-sinf (Dostobod)",
        "XOLMIRZAYEV SHERBEK 2-maktab 6-sinf (Chinoz)",
        "FURQATOVA PARIRUXSOR 14-maktab 6-sinf (Niyozbosh)",
        "ALIBEKOV ELNUR 12-maktab 4-sinf (Kids 2)",
        "ALIYEVA NIGINA 33-maktab 5-sinf (Paxtazor)",
        "EGAMBERDIYEV BEKMUROD 49-maktab 9-sinf (Kasblar maktabi)",
        "OBIDOV ISLOM 51-maktab 4A-sinf (Mevazor)",
        "ABDUGAPPAROV NURULLOH 55-maktab 8-sinf (Xalqobod)",
        "ORIFJONOV JASURBEK 13-maktab 6-sinf (Kids 1)",
        "PO‘LATBOYEV SARDOR 45-maktab 5-sinf (Gulbaxor)"
    ],

    ("English", "senior"): [
        "ABDUXALIKOVA MADINA 42-maktab 11-sinf (Olmazor)",
        "ISKANDAROVA MUSHTARIY 28-maktab 3-sinf (Xalqobod)",
        "TOHIROV XURSHID 11-maktab 11-sinf (Dostobod)",
        "ISMATULLAYEVA NARGIZA 50-maktab 9-sinf (Paxtazor)",
        "MAMURJONOV AZIZBEK 3-maktab 7-sinf (Kids 2)",
        "ABDUMANNOPOV ABDUXAMID 2-maktab 9B-sinf (Kasblar maktabi)",
        "ODILJONOV FOZILJON 36-maktab 8-sinf (Mevazor)",
        "XUJANOV ASILXAN 4-maktab 7-sinf (Chinoz)",
        "SHAVKATOVA RUXSHONA 23-maktab 8-sinf (Niyozbosh)",
        "BAXTIYOROVA BAHORA 14-maktab 7-sinf (Kids 1)",
        "ORIFJONOVA SOLIHA 1-maktab 8-sinf (Gulbaxor)"
    ],

    # (qolgan fanlar xuddi shu tartibda qoldi)
}

# ================== DATABASE ==================
def init_db():
    with sqlite3.connect(DB_NAME) as db:
        db.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            user_id INTEGER,
            subject TEXT,
            level TEXT,
            student TEXT,
            UNIQUE(user_id, subject, level)
        )
        """)
        db.execute("""
        CREATE TABLE IF NOT EXISTS voting (
            start_time INTEGER
        )
        """)

def start_voting():
    with sqlite3.connect(DB_NAME) as db:
        db.execute("DELETE FROM voting")
        db.execute("DELETE FROM votes")
        db.execute(
            "INSERT INTO voting (start_time) VALUES (?)",
            (int(time.time()),)
        )

def is_voting_active():
    with sqlite3.connect(DB_NAME) as db:
        row = db.execute(
            "SELECT start_time FROM voting ORDER BY start_time DESC LIMIT 1"
        ).fetchone()

    if not row:
        return False

    return time.time() < row[0] + VOTING_DURATION

# ================== BOT ==================
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ================== START ==================
@dp.message(Command("start"))
async def start(msg: types.Message):

    # 🔐 ADMIN
    if msg.from_user.id == ADMIN_ID:
        start_voting()
        await msg.answer(
            "✅ Ovoz berish BOSHLANDI!\n"
            "⏳ Davomiyligi: 7 kun"
        )
        return

    # 👤 USER
    if not is_voting_active():
        await msg.answer("⛔ Ovoz berish hozirda YOPIQ")
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1-kanal", url="https://t.me/azizacademy_uz")],
        [InlineKeyboardButton(text="2-kanal", url="https://t.me/codingwith_ulugbek")],
        [InlineKeyboardButton(text="✅ Obuna bo‘ldim", callback_data="check")]
    ])

    await msg.answer("Ikkala kanalga obuna bo‘ling:", reply_markup=kb)

# ================== OBUNA CHECK ==================
async def is_subscribed(user_id: int) -> bool:
    try:
        for ch in CHANNELS:
            member = await bot.get_chat_member(ch, user_id)
            if member.status not in ("member", "administrator", "creator"):
                return False
        return True
    except:
        return False

@dp.callback_query(lambda c: c.data == "check")
async def check(call: types.CallbackQuery):
    await call.answer()

    if not is_voting_active():
        await call.message.answer("⛔ Ovoz berish yakunlangan")
        return

    if not await is_subscribed(call.from_user.id):
        await call.message.answer("❌ Avval obuna bo‘ling")
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=s, callback_data=f"sub:{s}")]
        for s in SUBJECTS
    ])

    await call.message.answer("📚 Fanni tanlang:", reply_markup=kb)

# ================== FAN → SINF ==================
@dp.callback_query(lambda c: c.data.startswith("sub:"))
async def choose_class(call: types.CallbackQuery):
    await call.answer()
    subject = call.data.split(":")[1]

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("1–6 sinf", callback_data=f"class:{subject}:junior")],
        [InlineKeyboardButton("7–11 sinf", callback_data=f"class:{subject}:senior")]
    ])

    await call.message.answer("🎓 Sinfni tanlang:", reply_markup=kb)

# ================== O‘QUVCHILAR ==================
@dp.callback_query(lambda c: c.data.startswith("class:"))
async def show_students(call: types.CallbackQuery):
    await call.answer()
    _, subject, level = call.data.split(":")

    students = SPECIAL_STUDENTS.get((subject, level), [])

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=s, callback_data=f"vote:{subject}:{level}:{i}")]
        for i, s in enumerate(students)
    ])

    await call.message.answer("👨‍🎓 O‘quvchini tanlang:", reply_markup=kb)

# ================== OVOZ ==================
@dp.callback_query(lambda c: c.data.startswith("vote:"))
async def vote(call: types.CallbackQuery):
    await call.answer()

    if not is_voting_active():
        await call.message.answer("⛔ Ovoz berish yakunlangan")
        return

    _, subject, level, idx = call.data.split(":")
    idx = int(idx)

    students = SPECIAL_STUDENTS[(subject, level)]
    student = students[idx]

    try:
        with sqlite3.connect(DB_NAME) as db:
            db.execute(
                "INSERT INTO votes VALUES (?,?,?,?)",
                (call.from_user.id, subject, level, student)
            )
    except sqlite3.IntegrityError:
        await call.message.answer("⚠️ Siz allaqachon ovoz bergansiz")
        return

    with sqlite3.connect(DB_NAME) as db:
        rows = db.execute("""
            SELECT student, COUNT(*)
            FROM votes
            WHERE subject=? AND level=?
            GROUP BY student
        """, (subject, level)).fetchall()

    vote_map = dict(rows)
    total = sum(vote_map.values())

    text = f"📊 {subject} | {'1–6' if level=='junior' else '7–11'} sinf:\n\n"
    for s in students:
        c = vote_map.get(s, 0)
        p = (c / total * 100) if total else 0
        text += f"{s} — {c} ta ({p:.1f}%)\n"

    await call.message.answer("✅ Ovozingiz qabul qilindi!\n\n" + text)

# ================== RUN ==================
async def main():
    init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
