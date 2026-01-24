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
SPECIAL_STUDENTS = {

    # ================= ENGLISH =================
    ("English", "junior"): [
        "ALIBOYEVA SADOQAT (Olmazor)",
        "ULUGBEKOV FAYOZBEK (Dostobod)",
        "XOLMIRZAYEV SHERBEK (Chinoz)",
        "FURQATOVA PARIRUXSOR (Niyozbosh)",
        "ALIBEKOV ELNUR (Kids 2)",
        "ALIYEVA NIGINA (Paxtazor)",
        "EGAMBERDIYEV BEKMUROD (Kasblar maktabi)",
        "OBIDOV ISLOM (Mevazor)",
        "ABDUGAPPAROV NURULLOH (Xalqobod)",
        "ORIFJONOV JASURBEK (Kids 1)",
        "PO‘LATBOYEV SARDOR (Gulbaxor)"
    ],

    ("English", "senior"): [
        "ABDUXALIKOVA MADINA (Olmazor)",
        "ISKANDAROVA MUSHTARIY (Xalqobod)",
        "TOHIROV XURSHID (Dostobod)",
        "ISMATULLAYEVA NARGIZA (Paxtazor)",
        "MAMURJONOV AZIZBEK (Kids 2)",
        "ABDUMANNOPOV ABDUXAMID (Kasblar maktabi)",
        "ODILJONOV FOZILJON (Mevazor)",
        "XUJANOV ASILXAN (Chinoz)",
        "SHAVKATOVA RUXSHONA (Niyozbosh)",
        "BAXTIYOROVA BAHORA (Kids 1)",
        "ORIFJONOVA SOLIHA (Gulbaxor)"
    ],

    # ================= RUS =================
    ("Rus", "junior"): [
        "OBIDJONOVA MASUMA (Olmazor)",
        "AKBARALIYEV SHOXJAHON (Dostobod)",
        "RAXMONBERDIYEV IBROHIM (Chinoz)",
        "FAXRIDDINOV SHOXRUZ (Niyozbosh)",
        "AYTMUXAMMEDOVA MUBINA (Kids 2)",
        "NURIDDINOV BEXRUZ (Kasblar maktabi)",
        "TURDIBAYEVA MADINA (Mevazor)",
        "ALIMKULOVA SHIRIN (Xalqobod)",
        "XASANBOYEV SAMANDAR (Kids 1)",
        "Po’latboyev Sardor (Gulbahor)",
    ],

    ("Rus", "senior"): [
        "SHAVKATOVA SHABNAM (Olmazor)",
        "ABDUJABBAROVA SHIRIN (Xalqobod)",
        "ORIPBOYEV BERDIYOR (Dostobod)",
        "MARATOVA JASMINA (Paxtazor)",
        "MAMADALIYEV BEXRUZ (Kids 2)",
        "MAXSUDOVA SHAXZODA (Kasblar maktabi)",
        "EGAMKULOV ABBOS (Mevazor)",
        "ESENBEKOVA MAFTUNA (Chinoz)",
        "FAXRIDDINOV SHOXRUZ (Niyozbosh)",
        "OLIMBOYEVA PARIZODA (Kids 1)",
        "Orifjonova Soliha (Gulbahor)",
    ],

    # ================= KOREYS =================
    ("Koreys", "junior"): [
        "JUMANAZAROVA FARIZA (Olmazor)",
        "QURBONOV JASUR (Niyozbosh)",
        "ABDUQAYUMOV ANVAR (Kasblar maktabi)",
        "GOFURJONOVA NOZIMA (Gulbahor)",
    ],

    ("Koreys", "senior"): [
        "ARIKULOVA SHIRIN (Olmazor)",
        "ISTAMBEKOVA DILNOZA (Kasblar maktabi)",
        "ALISHEROVA SEVINCH (Chinoz)",
        "ASQAROVA SHIRIN (Niyozbosh)",
        "XABIBULLAYEVA MALIKA (Gulbahor)",
    ],

    # ================= ARABIC =================
    ("Arab", "junior"): [
        "GAYRATOV SHAMSHOD (Kasblar maktabi)",
        "MASHRAPOV SHOXRUZ (Mevazor)",
        "ABDUROUFOVA SHAXZODA (Xalqobod)",
        "TOXIRJONOVA DILYORA (Niyozbosh)",
        "RAZMATOVA AROFAR (Kids 2)",
        "XOLBOYEV AZIZJON (Chinoz)",
        "ABDUXALILOV ABUBAKIR (Kids 1)",
        "ISMOILJONOV  IBROXIM (Gulbahor)",
    ],

    ("Arab", "senior"): [
        "KOMILOV OZODBEK (Mevazor)",
        "MAXSUTALIYEVA MAFTUNA (Xalqobod)",
        "SOLIYEVA SHODIYAXON (Kasblar maktabi)",
        "YOQUBJONOVA UMIDA (Niyozbosh)",
        "ABDURAXMONOVA IRODA (Kids 2)",
        "XAMZAYEVA SUG‘DIYONA (Chinoz)",
        "MURODJONOVA E‘ZOZA (Kids 1)",
        "XABIBULLAYEVA MALIKA (Gulbahor)",
    ],

    # ================= MATEMATIKA =================
    ("Matematika", "junior"): [
        "ABDUJALILOV ANVARBEK (Olmazor)",
        "SHORASULOV SHOAZIM (Chinoz)",
        "ERMATOVA SAMIRA (Niyozbosh)",
        "BAXROMJONOV AVZALBEK (Kasblar maktabi)",
        "OBIDOV ISLOM (Mevazor)"
    ],

    ("Matematika", "senior"): [
        "SULAYMONOV OZODBEK (Olmazor)",
        "TURONOV OZODBEK (Dostobod)",
        "AXMADOV BARKAMOL (Kasblar maktabi)",
        "ABDUHAFIZOV NURBOL (Mevazor)",
        "RISBOYEVA XIDOYAT (Chinoz)",
        "ALISHEROV XASAN (Niyozbosh)"
    ],

    # ================= MENTAL =================
    ("Mental", "junior"): [
        "RAVSHANOV FAYZULLOX (Olmazor)",
        "LUKMANOV ABDULLOH (Kids 2)"
    ],

    ("Mental", "senior"): [
        "ALIXAYDAROV MANSUR (Olmazor)",
        "ABDUJABBOROVA MUSLIMA (Kids 2)"
    ],

    # ================= POCHEMUCHKA =================
    ("Pochemuchka", "junior"): [
        "MAXMUDOV ZIYODULLA (Olmazor)",
        "ABDUSALOMOVA DILZODA (Kids 2)",
        "BAXODIROVA UMIDA (Kasblar maktabi)"
    ],

    # ================= HAMSHIRALIK =================
    ("Hamshiralik", "junior"): [
        "RAVSHANOV FAYZULLOX (Olmazor)",
        "MAMARASULOVA DILRABO (Xalqobod)",
        "MAXAMADKARIMOVA FOTIMA (Kasblar maktabi)",
        "IBRAGIMOVA ZILOLA (Gulbahor)",
    ],

    ("Hamshiralik", "senior"): [
        "BAXODIROVA AZIZA (Olmazor)",
        "MIRGAYAZOVA MAFTUNA (Kids 2)",
        "ERGASHEVA RUXSHONA (Kasblar maktabi)",
        "ERGASHBAYEVA SARVINOZ (Mevazor)",
        "ABDUSODIQOVA SHAXZODA (Paxtazor)",
        "TOXIROVA SHAXZODA (Dostobod)",
        "SADRIDDINOVA MADINABONU (Chinoz)",
        "MANSUROVA UMIDA (Xalqobod)",
        "Sunnatillayeva Shodiya (Gulbahor)",
    ],

    # ================= IT =================
    ("IT", "junior"): [
        "DONIYOROV MUXAMMADALI (Olmazor)",
        "OLIMOV QALQONBEK (Xalqobod)",
        "YUSUPJONOV ROVSHAN (Kasblar maktabi)",
        "AXMEDOV KAMOLIDDIN (Chinoz)",
        "KALANDAROV ALISHER (Gulbahor)",
    ],

    ("IT", "senior"): [
        "QOBILJONOV FOZILJON (Olmazor)",
        "KOMILOV NURMUHAMMAD (Xalqobod)",
        "AYBEKOV DALER (Kasblar maktabi)",
        "SAIDALOMOV SAIDJAXON (Chinoz)",
        "UMURZOQOV SAMANDAR (Gulbahor)",
    ],

    # ================= KAMPYUTER =================
    ("Kampyuter", "junior"): [
        "ERKINOVA ASILABONU (Olmazor)",
        "AKBARALIYEV BEKZOD (Chinoz)",
        "ABDUKARIMOV SANJAR (Kasblar maktabi)",
        "KUZIYEV MUHAMMAD (Gulbahor)",
    ],

    ("Kampyuter", "senior"): [
        "SULTONMURODOV BEXRUZ (Olmazor)",
        "RAXMATULLAYEV UBAYDULLO (Chinoz)",
        "RASULOV DAVRON (Kasblar maktabi)",
        "ULUGBERDIYEV JAVLONBEK (Gulbahor)",
    ],

    # ================= LOYIHA =================
    ("Loyiha", "junior"): [
        "SHERALIYEV ISMOIL",
        "KOMILJONOV ZUXRIDDIN",
        "BAXTIYOROVA E'ZOZA",
        "TURSUNALIYEV NODIRBEK"
    ]
}
# ⚠️ SPECIAL_STUDENTS — SEN YUBORGAN HOLATDA QOLADI
# (joy tejash uchun bu yerda qisqartirildi)
# SENIKI O‘SHA-O‘SHA

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
async def is_subscribed(user_id):
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

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=s, callback_data=f"sub:{s}")]
            for s in SUBJECTS
        ]
    )
    await call.message.answer("📚 Fanni tanlang:", reply_markup=kb)

# ================== SINF ==================
@dp.callback_query(lambda c: c.data.startswith("sub:"))
async def choose_class(call: types.CallbackQuery):
    await call.answer()
    subject = call.data.split(":")[1]

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1–6 sinf", callback_data=f"class:{subject}:junior")],
        [InlineKeyboardButton(text="7–11 sinf", callback_data=f"class:{subject}:senior")]
    ])
    await call.message.answer("🎓 Sinfni tanlang:", reply_markup=kb)

# ================== O‘QUVCHILAR ==================
@dp.callback_query(lambda c: c.data.startswith("class:"))
async def show_students(call: types.CallbackQuery):
    await call.answer()
    _, subject, level = call.data.split(":")
    students = SPECIAL_STUDENTS.get((subject, level), [])

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=s, callback_data=f"vote:{subject}:{level}:{i}")]
            for i, s in enumerate(students)
        ]
    )
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

    vote_map = {s: c for s, c in rows}
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
