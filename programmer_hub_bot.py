import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command

# Bot tokeningiz
TOKEN = "8302735242:AAFsoQ9_eXejAY_L-njkiMpMnjPB_qQTP-I"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Foydalanuvchi holatlari
user_lang = {}   # {user_id: "uz"/"en"/"ru"/"tr"}
quiz_mode = {}   # {user_id: javob}

# Til va tugmalar matnlari
texts = {
    "start_msg": {
        "uz": "Assalomu alaykum! Tilni tanlang 👇",
        "en": "Hello! Choose your language 👇",
        "ru": "Здравствуйте! Выберите язык 👇",
        "tr": "Merhaba! Dilinizi seçin 👇"
    },
    "main_menu": {
        "uz": ["🐍 Python", "☕ Java", "💻 Frontend", "📝 Mini quiz", "🎲 Fun fact", "ℹ️ Bot haqida", "👑 Admin", "🎵 Musiqa"],
        "en": ["🐍 Python", "☕ Java", "💻 Frontend", "📝 Mini quiz", "🎲 Fun fact", "ℹ️ About Bot", "👑 Admin", "🎵 Music"],
        "ru": ["🐍 Python", "☕ Java", "💻 Фронтенд", "📝 Мини-викторина", "🎲 Факт", "ℹ️ О боте", "👑 Админ", "🎵 Музыка"],
        "tr": ["🐍 Python", "☕ Java", "💻 Frontend", "📝 Mini quiz", "🎲 İlginç bilgi", "ℹ️ Bot hakkında", "👑 Admin", "🎵 Müzik"]
    },
    "back": {"uz": "🔙 Orqaga", "en": "🔙 Back", "ru": "🔙 Назад", "tr": "🔙 Geri"},
    "choose_button": {
        "uz": "Quyidagi tugmalardan birini tanlang ⬇️",
        "en": "Choose a button below ⬇️",
        "ru": "Выберите кнопку ниже ⬇️",
        "tr": "Aşağıdaki butonlardan birini seçin ⬇️"
    }
}

# Bo‘limlarga matn tushuntirish
section_texts = {
    "Python": {
        "uz": "🐍 Python bo‘limi:\nPython oson o‘rganiladigan va mashhur dasturlash tili. Syntax sodda, AI va Data Science uchun keng ishlatiladi.",
        "en": "🐍 Python section:\nPython is an easy-to-learn, popular programming language. Simple syntax, widely used in AI and Data Science.",
        "ru": "🐍 Раздел Python:\nPython — простой и популярный язык программирования. Используется в AI и Data Science.",
        "tr": "🐍 Python bölümü:\nPython öğrenmesi kolay ve popüler bir programlama dili. Basit sözdizimi, AI ve Veri Bilimi için yaygın kullanılır."
    },
    "Java": {
        "uz": "☕ Java bo‘limi:\nJava — keng tarqalgan, obyektga yo‘naltirilgan dasturlash tili. Mobil va web ilovalar uchun ishlatiladi.",
        "en": "☕ Java section:\nJava is a popular object-oriented programming language, used for mobile and web applications.",
        "ru": "☕ Раздел Java:\nJava — популярный объектно-ориентированный язык программирования для мобильных и веб приложений.",
        "tr": "☕ Java bölümü:\nJava popüler bir nesne yönelimli programlama dilidir, mobil ve web uygulamaları için kullanılır."
    },
    "Frontend": {
        "uz": "💻 Frontend bo‘limi:\nFrontend web dasturlash — HTML, CSS va JavaScript yordamida saytning tashqi ko‘rinishi va interaktivligini yaratish.",
        "en": "💻 Frontend section:\nFrontend web development uses HTML, CSS, and JavaScript to create the appearance and interactivity of websites.",
        "ru": "💻 Раздел Frontend:\nFrontend веб-разработка использует HTML, CSS и JavaScript для внешнего вида и интерактивности сайта.",
        "tr": "💻 Frontend bölümü:\nFrontend web geliştirme, HTML, CSS ve JavaScript kullanarak web sitelerinin görünümünü ve etkileşimini oluşturur."
    },
    "Bot": {
        "uz": "ℹ️ Bot haqida:\nBu bot dasturlash bo‘limlarini o‘rganish, mini quiz orqali bilimni sinash va qiziqarli faktlar bilan tanishish uchun yaratilgan. "
              "Botning asosiy maqsadi foydalanuvchilarga Python, Java va Frontend bo‘limlari haqida ma’lumot berish, interaktiv quiz orqali bilimni mustahkamlash va foydali faktlar bilan qiziqtirishdir.\n\n"
              "Bo‘limlar:\n"
              "- Python: dasturlash tili tushunchasi va sintaksisi\n"
              "- Java: obyektga yo‘naltirilgan dasturlash tili\n"
              "- Frontend: HTML, CSS va JavaScript orqali web dizayn\n"
              "- Mini quiz: bilimlarni sinash\n"
              "- Fun fact: qiziqarli faktlar\n"
              "- Admin: botning admini\n"
              "- Musiqa: boshqa botlar bilan ishlash imkoniyati",
        "en": "ℹ️ About Bot:\nThis bot is created to learn programming sections, test knowledge with mini quizzes, and explore fun facts. "
              "The main purpose is to provide information about Python, Java, and Frontend, strengthen knowledge with interactive quizzes, and share useful facts.\n\n"
              "Sections:\n"
              "- Python: programming language and syntax\n"
              "- Java: object-oriented programming language\n"
              "- Frontend: web design with HTML, CSS, and JavaScript\n"
              "- Mini quiz: test your knowledge\n"
              "- Fun fact: interesting facts\n"
              "- Admin: bot admin\n"
              "- Music: interact with other bots",
        "ru": "ℹ️ О боте:\nЭтот бот создан для изучения разделов программирования, проверки знаний через мини-викторину и знакомства с интересными фактами. "
              "Основная цель — предоставить информацию о Python, Java и Frontend, укрепить знания через интерактивные викторины и поделиться полезными фактами.\n\n"
              "Разделы:\n"
              "- Python: язык программирования и синтаксис\n"
              "- Java: объектно-ориентированный язык программирования\n"
              "- Frontend: веб-дизайн с использованием HTML, CSS и JavaScript\n"
              "- Мини-викторина: проверка знаний\n"
              "- Факт: интересные факты\n"
              "- Админ: администратор бота\n"
              "- Музыка: работа с другими ботами",
        "tr": "ℹ️ Bot hakkında:\nBu bot, programlama bölümlerini öğrenmek, mini quiz ile bilgiyi test etmek ve ilginç bilgiler keşfetmek için oluşturuldu. "
              "Ana amaç, Python, Java ve Frontend hakkında bilgi sağlamak, interaktif quizlerle bilgiyi pekiştirmek ve faydalı bilgiler sunmaktır.\n\n"
              "Bölümler:\n"
              "- Python: programlama dili ve sözdizimi\n"
              "- Java: nesne yönelimli programlama dili\n"
              "- Frontend: HTML, CSS ve JavaScript ile web tasarım\n"
              "- Mini quiz: bilginizi test edin\n"
              "- Fun fact: ilginç bilgiler\n"
              "- Admin: bot admini\n"
              "- Müzik: diğer botlarla etkileşim"
    }
}

# Mini quiz
quiz = [
    {"savol": {"uz": "Python nima uchun mashhur?", "en": "Why is Python popular?", "ru": "Почему Python популярен?", "tr": "Python neden popüler?"},
     "javob": {"uz": "Oson va qulay sintaksis, AI va Data Science sohalari uchun", "en": "Easy syntax, used in AI and Data Science", "ru": "Простой синтаксис, используется в AI и Data Science", "tr": "Kolay sözdizimi, AI ve Veri Bilimi için kullanılır"}}
]

# Fun fact
fun_facts = {
    "uz": ["🐍 Python nomi Monty Python’dan ilhomlangan!"],
    "en": ["🐍 Python is named after Monty Python!"],
    "ru": ["🐍 Python назван в честь Монти Пайтона!"],
    "tr": ["🐍 Python adı Monty Python'dan geliyor!"]
}

# Til tanlash tugmalari
def language_keyboard():
    buttons = [
        [KeyboardButton(text="🇺🇿 O‘zbekcha"), KeyboardButton(text="🇬🇧 English")],
        [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇹🇷 Türkçe")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# Asosiy menyu tugmalari
def main_menu_keyboard(lang):
    buttons = texts["main_menu"][lang]
    keyboard = []
    for i in range(0, len(buttons), 2):
        if i+1 < len(buttons):
            keyboard.append([KeyboardButton(text=buttons[i]), KeyboardButton(text=buttons[i+1])])
        else:
            keyboard.append([KeyboardButton(text=buttons[i])])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# /start komandasi
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(texts["start_msg"]["uz"], reply_markup=language_keyboard())

# Xabarlarni qabul qilish
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    # Til tanlash
    if text in ["🇺🇿 O‘zbekcha", "🇬🇧 English", "🇷🇺 Русский", "🇹🇷 Türkçe"]:
        lang_map = {"🇺🇿 O‘zbekcha":"uz","🇬🇧 English":"en","🇷🇺 Русский":"ru","🇹🇷 Türkçe":"tr"}
        user_lang[user_id] = lang_map[text]
        await message.answer(f"✅ Ok! Til: {text}", reply_markup=main_menu_keyboard(user_lang[user_id]))
        return

    lang = user_lang.get(user_id)
    if not lang:
        await message.answer("❗ Iltimos, avval tilni tanlang 👇", reply_markup=language_keyboard())
        return

    # Mini quiz
    if text in ["Mini quiz", "📝 Mini quiz", "Мини-викторина"]:
        q = random.choice(quiz)
        quiz_mode[user_id] = q["javob"][lang]
        await message.answer(f"📝 {q['savol'][lang]}\n\nJavobini yozing:", reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=texts["back"][lang])]],
            resize_keyboard=True
        ))
        return

    # Fun fact
    if text in ["Fun fact", "🎲 Fun fact", "Факт", "İlginç bilgi"]:
        fact = random.choice(fun_facts[lang])
        await message.answer(f"🎲 Fun fact:\n{fact}", reply_markup=main_menu_keyboard(lang))
        return

    # Orqaga tugma
    if text == texts["back"][lang]:
        await message.answer(texts["choose_button"][lang], reply_markup=main_menu_keyboard(lang))
        quiz_mode.pop(user_id, None)
        return

    # Bo‘limlar
    if text in texts["main_menu"][lang]:
        if text in ["🐍 Python", "Python"]:
            await message.answer(section_texts["Python"][lang], reply_markup=main_menu_keyboard(lang))
        elif text in ["☕ Java", "Java"]:
            await message.answer(section_texts["Java"][lang], reply_markup=main_menu_keyboard(lang))
        elif text in ["💻 Frontend", "Frontend"]:
            await message.answer(section_texts["Frontend"][lang], reply_markup=main_menu_keyboard(lang))
        elif text in ["ℹ️ Bot haqida", "About Bot", "О боте", "Bot hakkında"]:
            await message.answer(section_texts["Bot"][lang], reply_markup=main_menu_keyboard(lang))
        elif text in ["👑 Admin", "Admin"]:
            await message.answer(
                f"👑 Admin bo‘limi\nBotning admini: @XAKING_A\nYaratilgan sana: 13-oktyabr-2025",
                reply_markup=main_menu_keyboard(lang)
            )
        elif text in ["🎵 Musiqa", "Music"]:
            await message.answer(
                f"🎵 Musiqa bo‘limi\nSiz tinglashingiz mumkin bo‘lgan bot: @uz_musiqa_bot",
                reply_markup=main_menu_keyboard(lang)
            )
        return

    # Default javob
    await message.answer(texts["choose_button"][lang], reply_markup=main_menu_keyboard(lang))

# Bot ishga tushirish
async def main():
    print("✅ Bot ishga tushdi")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
