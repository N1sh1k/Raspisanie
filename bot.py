import json
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Токен от BotFather
API_TOKEN = 'Токен'

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def load_schedule_for_group(group_name):
    """Ищет пары в JSON-файле для конкретной группы."""
    try:
        with open('data/result.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Фильтрация данных JSON
        results = [item['lesson'] for item in data if group_name.upper() in item['group'].upper()]
        return results
    except Exception as e:
        return [f"Ошибка чтения базы: {e}"]

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот АППК. Напиши мне номер группы (например, ТМ-21), и я выдам расписание!")

@dp.message()
async def get_schedule(message: types.Message):
    group = message.text.strip()
    lessons = load_schedule_for_group(group)
    
    if lessons:
        text = f"📅 Расписание для {group}:\n" + "\n".join([f"• {l}" for l in lessons])
    else:
        text = f"Группа {group} не найдена в текущем расписании."
    
    await message.answer(text)

async def main():
    print("🤖 Бот запущен и ждет сообщений...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())