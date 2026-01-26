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

# ================== O‘QUVCHILAR (QISQARTIRILDI) ==================
SPECIAL_STUDENTS = {

    # ================= ENGLISH =================
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
d
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

    # ================= RUS =================
    ("Rus", "junior"): [
        "OBIDJONOVA MASUMA 29-maktab 8-sinf (Olmazor)",
        "AKBARALIYEV SHOXJAHON 24-maktab 6-sinf (Dostobod)",
        "RAXMONBERDIYEV IBROHIM 2-maktab 3-sinf (Chinoz)",
        "FAXRIDDINOV SHOXRUZ 5-maktab 4-sinf (Niyozbosh)",
        "AYTMUXAMMEDOVA MUBINA 3-maktab 6-sinf (Kids 2)",
        "NURIDDINOV BEXRUZ 1-maktab 4-sinf (Kasblar maktabi)",
        "TURDIBAYEVA MADINA 51-maktab 5B-sinf (Mevazor)",
        "ALIMKULOVA SHIRIN 19-maktab 7-sinf (Xalqobod)",
        "XASANBOYEV SAMANDAR 1-maktab 4-sinf (Kids 1)",
        "PO‘LATBOYEV SARDOR 45-maktab 5-sinf (Gulbahor)"
    ],

    ("Rus", "senior"): [
        "SHAVKATOVA SHABNAM 15-maktab 8-sinf (Olmazor)",
        "ABDUJABBAROVA SHIRIN 28-maktab 8-sinf (Xalqobod)",
        "ORIPBOYEV BERDIYOR 10-maktab 11-sinf (Dostobod)",
        "MARATOVA JASMINA 50-maktab 7-sinf (Paxtazor)",
        "MAMADALIYEV BEXRUZ 1-maktab 10-sinf (Kids 2)",
        "MAXSUDOVA SHAXZODA 6-maktab 8-sinf (Kasblar maktabi)",
        "EGAMKULOV ABBOS 34-maktab 6-sinf (Mevazor)",
        "ESENBEKOVA MAFTUNA 11-maktab 10-sinf (Chinoz)",
        "FAXRIDDINOV SHOXRUZ 5-maktab 4-sinf (Niyozbosh)",
        "OLIMBOYEVA PARIZODA 14-maktab 7-sinf (Kids 1)",
        "ORIFJONOVA SOLIHA 1-maktab 8-sinf (Gulbahor)"
    ],

    # ================= KOREYS =================
    ("Koreys", "junior"): [
        "JUMANAZAROVA FARIZA 9-maktab 3-sinf (Olmazor)",
        "QURBONOV JASUR 33-maktab 4-sinf (Niyozbosh)",
        "ABDUQAYUMOV ANVAR 6-maktab 7-sinf (Kasblar maktabi)",
        "GOFURJONOVA NOZIMA 1-maktab 7-sinf (Gulbahor)"
    ],

    ("Koreys", "senior"): [
        "ARIKULOVA SHIRIN 5-maktab 11-sinf (Olmazor)",
        "ISTAMBEKOVA DILNOZA 6-maktab 11-sinf (Kasblar maktabi)",
        "ALISHEROVA SEVINCH 26-maktab 7-sinf (Chinoz)",
        "ASQAROVA SHIRIN IDUM 8-sinf (Niyozbosh)",
        "XABIBULLAYEVA MALIKA 44-maktab 7-sinf (Gulbahor)"
    ],

    # ================= ARAB =================
    ("Arab", "junior"): [
        "GAYRATOV SHAMSHOD 5-maktab 4-sinf (Kasblar maktabi)",
        "MASHRAPOV SHOXRUZ 33-maktab 3V-sinf (Mevazor)",
        "ABDUROUFOVA SHAXZODA 28-maktab 7-sinf (Xalqobod)",
        "TOXIRJONOVA DILYORA 1-maktab 5-sinf (Niyozbosh)",
        "RAZMATOVA AROFAR 3-maktab 5-sinf (Kids 2)",
        "XOLBOYEV AZIZJON 13-maktab 5-sinf (Chinoz)",
        "ABDUXALILOV ABUBAKIR 0-maktab 0-sinf (Kids 1)",
        "ISMOILJONOV IBROXIM 45-maktab 6-sinf (Gulbahor)"
    ],

    ("Arab", "senior"): [
        "KOMILOV OZODBEK noma'lum-maktab noma'lum-sinf (Mevazor)",
        "MAXSUTALIYEVA MAFTUNA 28-maktab 8-sinf (Xalqobod)",
        "SOLIYEVA SHODIYAXON 13-maktab 11-sinf (Kasblar maktabi)",
        "YOQUBJONOVA UMIDA 23-maktab 9-sinf (Niyozbosh)",
        "ABDURAXMONOVA IRODA 27-maktab 11-sinf (Kids 2)",
        "XAMZAYEVA SUG‘DIYONA 40-maktab 10-sinf (Chinoz)",
        "MURODJONOVA E‘ZOZA 1-maktab 8-sinf (Kids 1)",
        "XABIBULLAYEVA MALIKA 44-maktab 7-sinf (Gulbahor)"
    ],

    # ================= MATEMATIKA =================
    ("Matematika", "junior"): [
        "ABDUJALILOV ANVARBEK noma'lum-maktab noma'lum-sinf (Olmazor)",
        "SHORASULOV SHOAZIM 40-maktab 5-sinf (Chinoz)",
        "ERMATOVA SAMIRA 9-maktab 6-sinf (Niyozbosh)",
        "BAXROMJONOV AVZALBEK 6-maktab 4-sinf (Kasblar maktabi)",
        "OBIDOV ISLOM 51-maktab 4A-sinf (Mevazor)"
    ],

    ("Matematika", "senior"): [
        "SULAYMONOV OZODBEK 46-maktab 11-sinf (Olmazor)",
        "TURONOV OZODBEK noma'lum-maktab noma'lum-sinf (Dostobod)",
        "AXMADOV BARKAMOL 9-maktab 8-sinf (Kasblar maktabi)",
        "ABDUHAFIZOV NURBOL 36-maktab 7-sinf (Mevazor)",
        "RISBOYEVA XIDOYAT 2-maktab 11-sinf (Chinoz)",
        "ALISHEROV XASAN 27-maktab 7-sinf (Niyozbosh)"
    ],

    # ================= MENTAL =================
    ("Mental", "junior"): [
        "RAVSHANOV FAYZULLOX 46-maktab 5-sinf (Olmazor)",
        "LUKMANOV ABDULLOH 3-maktab 4-sinf (Kids 2)"
    ],

    ("Mental", "senior"): [
        "ALIXAYDAROV MANSUR 9-maktab 6-sinf (Olmazor)",
        "ABDUJABBOROVA MUSLIMA 44-maktab 6-sinf (Kids 2)"
    ],

    # ================= POCHEMUCHKA =================
    ("Pochemuchka", "junior"): [
        "MAXMUDOV ZIYODULLA 0-maktab 0-sinf (Olmazor)",
        "ABDUSALOMOVA DILZODA noma'lum-maktab noma'lum-sinf (Kids 2)",
        "BAXODIROVA UMIDA 0-maktab 0-sinf (Kasblar maktabi)"
    ],

    # ================= HAMSHIRALIK =================
    ("Hamshiralik", "junior"): [
        "RAVSHANOV FAYZULLOX 46-maktab 5-sinf (Olmazor)",
        "MAMARASULOVA DILRABO 56-maktab 10-sinf (Xalqobod)",
        "MAXAMADKARIMOVA FOTIMA 0-maktab 0-sinf (Kasblar maktabi)",
        "IBRAGIMOVA ZILOLA 1-maktab 10-sinf (Gulbahor)"
    ],

    ("Hamshiralik", "senior"): [
        "BAXODIROVA AZIZA 9-maktab 10-sinf (Olmazor)",
        "MIRGAYAZOVA MAFTUNA noma'lum-maktab noma'lum-sinf (Kids 2)",
        "ERGASHEVA RUXSHONA 0-maktab 0-sinf (Kasblar maktabi)",
        "ERGASHBAYEVA SARVINOZ 36-maktab 10A-sinf (Mevazor)",
        "ABDUSODIQOVA SHAXZODA 46-maktab 10-sinf (Paxtazor)",
        "TOXIROVA SHAXZODA 11-maktab 10-sinf (Dostobod)",
        "SADRIDDINOVA MADINABONU 23-maktab 9-sinf (Chinoz)",
        "MANSUROVA UMIDA Bitirgan (Xalqobod)",
        "SUNNATILLAYEVA SHODIYA 48-maktab 10-sinf (Gulbahor)"
    ],

    # ================= IT =================
    ("IT", "junior"): [
        "DONIYOROV MUXAMMADALI 9-maktab 7-sinf (Olmazor)",
        "OLIMOV QALQONBEK 56-maktab 7-sinf (Xalqobod)",
        "YUSUPJONOV ROVSHAN 3-maktab 8-sinf (Kasblar maktabi)",
        "AXMEDOV KAMOLIDDIN 9-maktab 6-sinf (Chinoz)",
        "KALANDAROV ALISHER 5-maktab 6-sinf (Gulbahor)"
    ],

    ("IT", "senior"): [
        "QOBILJONOV FOZILJON 42-maktab 11-sinf (Olmazor)",
        "KOMILOV NURMUHAMMAD 28-maktab 8-sinf (Xalqobod)",
        "AYBEKOV DALER 2-maktab 8-sinf (Kasblar maktabi)",
        "SAIDALOMOV SAIDJAXON 2-maktab 9-sinf (Chinoz)",
        "UMURZOQOV SAMANDAR 1-maktab 8-sinf (Gulbahor)"
    ],

    # ================= KAMPYUTER =================
    ("Kampyuter", "junior"): [
        "ERKINOVA ASILABONU 17-maktab 5-sinf (Olmazor)",
        "AKBARALIYEV BEKZOD 9-maktab 5-sinf (Chinoz)",
        "ABDUKARIMOV SANJAR 14-maktab 9-sinf (Kasblar maktabi)",
        "KUZIYEV MUHAMMAD 1-maktab 6-sinf (Gulbahor)"
    ],

    ("Kampyuter", "senior"): [
        "SULTONMURODOV BEXRUZ 15-maktab 9-sinf (Olmazor)",
        "RAXMATULLAYEV UBAYDULLO 40-maktab 7-sinf (Chinoz)",
        "RASULOV DAVRON 10-maktab 7-sinf (Kasblar maktabi)",
        "ULUGBERDIYEV JAVLONBEK 48-maktab 7-sinf (Gulbahor)"
    ],

    # ================= LOYIHA =================
    ("Loyiha", "junior"): [
        "SHERALIYEV ISMOIL 27-maktab 1-sinf",
        "KOMILJONOV ZUXRIDDIN 11-maktab 2-sinf",
        "BAXTIYOROVA E'ZOZA 27-maktab 3-sinf",
        "TURSUNALIYEV NODIRBEK 16-maktab 4-sinf"
    ]
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

# ================== VAQT LOGIKASI ==================
def get_start_time():
    with sqlite3.connect(DB_NAME) as db:
        row = db.execute(
            "SELECT start_time FROM voting ORDER BY start_time ASC LIMIT 1"
        ).fetchone()
        return row[0] if row else None


def start_voting_once():
    if get_start_time() is not None:
        return False

    with sqlite3.connect(DB_NAME) as db:
        db.execute(
            "INSERT INTO voting (start_time) VALUES (?)",
            (int(time.time()),)
        )
    return True


def get_remaining_time():
    start_time = get_start_time()
    if not start_time:
        return "⛔ Ovoz berish boshlanmagan"

    remaining = int(start_time + VOTING_DURATION - time.time())
    if remaining <= 0:
        return "⛔ Ovoz berish yakunlangan"

    days = remaining // 86400
    hours = (remaining % 86400) // 3600
    minutes = (remaining % 3600) // 60

    return f"⏳ Qolgan vaqt: {days} kun {hours} soat {minutes} minut"


def is_voting_active():
    start_time = get_start_time()
    if not start_time:
        return False
    return time.time() < start_time + VOTING_DURATION

# ================== BOT ==================
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ================== START ==================
@dp.message(Command("start"))
async def start(msg: types.Message):
    remaining = get_remaining_time()

    # 🔐 ADMIN
    if msg.from_user.id == ADMIN_ID:
        started = start_voting_once()

        if started:
            await msg.answer(
                "✅ Ovoz berish BOSHLANDI!\n\n" + remaining
            )
        else:
            await msg.answer(
                "⚠️ Ovoz berish allaqachon BOSHLANGAN!\n\n" + remaining
            )
        return

    # 👤 USER
    if get_start_time() is None:
        await msg.answer("⛔ Ovoz berish hozirda YOPIQ")
        return

    await msg.answer(
        "✅ Ovoz berish BOSHLANGAN!\n\n" + remaining
    )

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

# ================== RUN ==================
async def main():
    init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
