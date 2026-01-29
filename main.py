import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

API_TOKEN = "8529829764:AAFAGUUJoHbqUMxK6_Si6nNNKEqez78nR8w"
CHANNEL_USERNAME = "@kali_linux09"
ADMIN_USERNAME = "Islompro_maxx"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

users = set()

async def add_user(user_id, username):
    if user_id not in users:
        users.add(user_id)

# --- Kanalga obuna tekshirish funksiyasi ---
async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status not in ["left", "kicked"]
    except Exception:
        return False

# --- START handler ---
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    if not await check_subscription(message.from_user.id):
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton("✅ Obuna bo‘ldim"))
        await message.answer(
            f"❌ Bot ishlashi uchun kanalga obuna bo‘ling: https://t.me/{CHANNEL_USERNAME[1:]}\n"
            "Obuna bo‘lgach quyidagi tugmani bosing",
            reply_markup=kb
        )
        return

    await add_user(message.from_user.id, message.from_user.username)
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📋 Admin menyu"))
    kb.add(KeyboardButton("💻 Bot haqida"))
    kb.add(KeyboardButton("📣 Kanalimiz haqida"))
    await message.answer("✅ Xush kelibsiz!", reply_markup=kb)

# --- Menu handler ---
@dp.message_handler()
async def menu_handler(message: types.Message):
    user_id = message.from_user.id

    # Kanalga obuna bo‘lish sharti
    if not await check_subscription(user_id):
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton("✅ Obuna bo‘ldim"))
        await message.answer(
            f"❌ Bot ishlashi uchun kanalga obuna bo‘ling: https://t.me/{CHANNEL_USERNAME[1:]}\n"
            "Obuna bo‘lgach tugmani yana bosing",
            reply_markup=kb
        )
        return

    text = message.text

    # ✅ Obuna bo‘ldim tugmasi
    if text == "✅ Obuna bo‘ldim":
        await message.answer("✅ Obuna tekshirildi! Endi botga kirishingiz mumkin.")
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton("📋 Admin menyu"))
        kb.add(KeyboardButton("💻 Bot haqida"))
        kb.add(KeyboardButton("📣 Kanalimiz haqida"))
        await message.answer("✅ Xush kelibsiz!", reply_markup=kb)
        await add_user(user_id, message.from_user.username)
        return

    # Foydalanuvchi menyusi
    elif text == "💻 Bot haqida":
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton("🔙 Orqaga qaytish"))
        await message.answer(
            "💻 Bu bot sizga quyidagilarni qilish imkonini beradi:\n\n"
            "• Admin bilan bog‘lanish\n"
            "• Foydalanuvchi sonini ko‘rish\n"
            "• Boshqa foydali bo‘limlar (faqat admin uchun)\n\n"
            "Bot doimiy yangilanadi va sizga qulay xizmat ko‘rsatadi!",
            reply_markup=kb
        )

    elif text == "📣 Kanalimiz haqida":
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton("🔙 Orqaga qaytish"))
        await message.answer(
            f"📣 Bizning Telegram kanalimiz: {CHANNEL_USERNAME}\n\n"
            "Kanalda siz quyidagilarni topishingiz mumkin:\n"
            "• C++ va Python bot code-lari\n"
            "• Dasturlash bo‘yicha foydali materiallar\n"
            "• Yangiliklar va amaliy loyihalar\n"
            "• Maslahatlar va yordam\n\n"
            "Obuna bo‘ling va yangi materiallardan birinchi bo‘lib xabardor bo‘ling!",
            reply_markup=kb
        )

    elif text == "🔙 Orqaga qaytish":
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton("📋 Admin menyu"))
        kb.add(KeyboardButton("💻 Bot haqida"))
        kb.add(KeyboardButton("📣 Kanalimiz haqida"))
        await message.answer("✅ Asosiy menyuga qaytdingiz", reply_markup=kb)

    # Admin menyu
    elif text == "📋 Admin menyu":
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.row(KeyboardButton("1️⃣ Tolov"), KeyboardButton("2️⃣ Menyu"))
        kb.row(KeyboardButton("3️⃣ Bot code sotib olish"), KeyboardButton("4️⃣ Donat qilish"))
        kb.row(KeyboardButton("5️⃣ Admin bilan bog‘lanish"), KeyboardButton("🔙 Orqaga qaytish"))
        await message.answer("📋 Admin menyu:", reply_markup=kb)

    # Admin menyu tugmalari
    elif text == "1️⃣ Tolov":
        await message.answer("💳 To‘lov qilish uchun karta raqami:\n\n7777 0111 6318 6748")

    elif text == "2️⃣ Menyu":
        await message.answer("📂 Menyu bo‘limi ishlayapti")

    elif text == "3️⃣ Bot code sotib olish":
        await message.answer(
            "💻 Bot code Telegram kanalimizda olasiz:\n"
            "https://t.me/kali_linux09"
        )

    elif text == "4️⃣ Donat qilish":
        await message.answer("💳 Donat qilish uchun karta raqami:\n\n7777 0111 6318 6748")

    elif text == "5️⃣ Admin bilan bog‘lanish":
        await message.answer(f"📞 Admin bilan bog‘lanish: @{ADMIN_USERNAME}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)





