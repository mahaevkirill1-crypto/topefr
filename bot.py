import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice, PreCheckoutQuery

# Берем токен из переменной окружения (на GitHub это будет секрет)
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- ВРЕМЕННОЕ ХРАНИЛИЩЕ (при перезапуске всё сотрется) ---
# Для теста этого хватит. Потом заменишь на SQLite или JSON-файл.
user_city = {}       # Кто какой город выбрал: {id_пользователя: "sovgavan"}
user_notify = {}     # Кто купил уведомления: {id_пользователя: True}
station_status = {}  # Статус заправок: {"sovgavan": [{"name": "...", "addr": "...", "status": "...", "time": "..."}]}

# --- СТАРТ БОТА ---
@dp.message(Command("start"))
async def start(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏙 Советская Гавань", callback_data="city_sovgavan")],
        [InlineKeyboardButton(text="🏙 Ванино", callback_data="city_vanino")]
    ])
    await message.answer("Выбери свой город:", reply_markup=kb)

# --- ВЫБОР ГОРОДА ---
@dp.callback_query(F.data.startswith("city_"))
async def set_city(cb: CallbackQuery):
    city = cb.data.replace("city_", "")
    user_city[cb.from_user.id] = city
    city_name = "Советская Гавань" if city == "sovgavan" else "Ванино"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔍 Посмотреть заправки", callback_data="view")],
        [InlineKeyboardButton(text="✍️ Сообщить о заправке", callback_data="report")],
        [InlineKeyboardButton(text="🔔 Купить уведомления (50⭐)", callback_data="buy_notify")]
    ])
    await cb.message.edit_text(f"Город: {city_name}\n\nЧто делаем?", reply_markup=kb)
    await cb.answer()

# --- ПОСМОТРЕТЬ СТАТУС ЗАПРАВОК ---
@dp.callback_query(F.data == "view")
async def view(cb: CallbackQuery):
    city = user_city.get(cb.from_user.id)
    if not city:
        await cb.answer("Сначала выбери город (нажми /start)")
        return
        
    stations = station_status.get(city, [])
    if not stations:
        await cb.message.answer("Пока нет данных по заправкам. Будь первым — нажми «Сообщить»!")
    else:
        # Формируем красивый список
        text = "\n".join([f"{s['status']} *{s['name']}* ({s['addr']}) — обновлено {s['time']}" for s in stations])
        await cb.message.answer(text, parse_mode="Markdown")
    await cb.answer()

# --- СООБЩИТЬ О ЗАПРАВКЕ (ШАГ 1: просим текст) ---
@dp.callback_query(F.data == "report")
async def report_start(cb: CallbackQuery):
    await cb.message.answer("Напиши название и адрес заправки через запятую.\nПример: `Трансбункер, ул. Ленина 5`", parse_mode="Markdown")
    await cb.answer()

# --- СООБЩИТЬ О ЗАПРАВКЕ (ШАГ 2: ловим текст с запятой) ---
@dp.message(F.text.contains(","))
async def receive_report(message: Message):
    city = user_city.get(message.from_user.id)
    if not city:
        await message.answer("Сначала выбери город (нажми /start)")
        return
        
    parts = message.text.split(",", 1)
    if len(parts) < 2:
        return
        
    name = parts[0].strip()
    addr = parts[1].strip()
    
    # Для простоты ставим статус "Есть". Позже сделаешь кнопки (Есть / Нет / Очередь)
    station_status.setdefault(city, []).append({
        "name": name, 
        "addr": addr, 
        "status": "✅ Есть", 
        "time": "только что"
    })
    
    await message.answer(f"Спасибо! Добавлено: {name} ({addr}) — ✅ Есть")

# --- ПОКУПКА УВЕДОМЛЕНИЙ ---
@dp.callback_query(F.data == "buy_notify")
async def buy_notify(cb: CallbackQuery):
    await bot.send_invoice(
        chat_id=cb.message.chat.id,
        title="Уведомления о бензине",
        description="30 дней уведомлений, когда на заправках появляется топливо",
        payload="notify_30d",
        provider_token="",  # Для Stars ВСЕГДА пустая строка
        currency="XTR",     # Код валюты Telegram Stars
        prices=[LabeledPrice(label="30 дней", amount=50)], # 50 звезд
        subscription_period=2592000  # 30 дней в секундах
    )
    await cb.answer()

# --- ПОДТВЕРЖДЕНИЕ ОПЛАТЫ (Telegram требует ответить за 10 секунд) ---
@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await query.answer(ok=True)

# --- УСПЕШНАЯ ОПЛАТА (включаем уведомления) ---
@dp.message(F.successful_payment)
async def payment_ok(message: Message):
    user_notify[message.from_user.id] = True
    await message.answer("✅ Уведомления активированы на 30 дней! Когда кто-то сообщит о бензине, я пришлю пуш.")

# --- ЗАПУСК ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
