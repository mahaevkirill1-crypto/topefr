import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice, PreCheckoutQuery

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хранилище
user_city = {}       
user_notify = {}     
station_status = {}  
temp_station = {}    # Временное хранилище для названия заправки перед выбором статуса

@dp.message(Command("start"))
async def start(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏙 Советская Гавань", callback_data="city_sovgavan")],
        [InlineKeyboardButton(text="🏙 Ванино", callback_data="city_vanino")]
    ])
    await message.answer("Выбери свой город:", reply_markup=kb)

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

@dp.callback_query(F.data == "view")
async def view(cb: CallbackQuery):
    city = user_city.get(cb.from_user.id)
    if not city:
        await cb.answer("Сначала выбери город (нажми /start)")
        return
        
    stations = station_status.get(city, [])
    if not stations:
        text = "Пока нет данных по заправкам. Будь первым — нажми «Сообщить»!"
    else:
        text = "📍 *Актуальные данные:*\n\n"
        for s in stations:
            text += f"{s['status']} *{s['name']}* ({s['addr']}) — {s['time']}\n"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Обновить", callback_data="view")]
    ])
    await cb.message.edit_text(text, parse_mode="Markdown", reply_markup=kb)
    await cb.answer()

@dp.callback_query(F.data == "report")
async def report_start(cb: CallbackQuery):
    await cb.message.edit_text("Напиши название и адрес заправки через запятую.\nПример: `Трансбункер, ул. Ленина 5`", parse_mode="Markdown")
    await cb.answer()

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
    
    # Сохраняем во временное хранилище
    temp_station[message.from_user.id] = {"name": name, "addr": addr}
    
    # Спрашиваем статус кнопками
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Есть бензин", callback_data="status_yes")],
        [InlineKeyboardButton(text="⏳ Очередь", callback_data="status_queue")],
        [InlineKeyboardButton(text="❌ Нет бензина", callback_data="status_no")]
    ])
    await message.answer(f"Заправка: {name} ({addr}).\nЧто там сейчас?", reply_markup=kb)

@dp.callback_query(F.data.startswith("status_"))
async def set_status(cb: CallbackQuery):
    status_type = cb.data.replace("status_", "")
    station = temp_station.get(cb.from_user.id)
    city = user_city.get(cb.from_user.id)
    
    if not station or not city:
        await cb.answer("Ошибка. Нажми /start")
        return

    status_text = {
        "yes": "✅ Есть", 
        "queue": "⏳ Очередь", 
        "no": "❌ Нет"
    }[status_type]
    
    # Проверяем, есть ли уже такая заправка, чтобы не дублировать
    stations = station_status.setdefault(city, [])
    existing = next((s for s in stations if s['name'].lower() == station['name'].lower()), None)
    
    if existing:
        existing['status'] = status_text
        existing['time'] = "только что"
    else:
        stations.append({
            "name": station['name'], 
            "addr": station['addr'], 
            "status": status_text, 
            "time": "только что"
        })
        
    del temp_station[cb.from_user.id]
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔍 Посмотреть заправки", callback_data="view")]
    ])
    await cb.message.edit_text(f"✅ Спасибо! Заправка *{station['name']}* обновлена: {status_text}", parse_mode="Markdown", reply_markup=kb)
    await cb.answer()

@dp.callback_query(F.data == "buy_notify")
async def buy_notify(cb: CallbackQuery):
    await bot.send_invoice(
        chat_id=cb.message.chat.id,
        title="Уведомления о бензине",
        description="30 дней уведомлений, когда на заправках появляется топливо",
        payload="notify_30d",
        provider_token="", 
        currency="XTR",
        prices=[LabeledPrice(label="30 дней", amount=50)],
        subscription_period=2592000 
    )
    await cb.answer()

@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await query.answer(ok=True)

@dp.message(F.successful_payment)
async def payment_ok(message: Message):
    user_notify[message.from_user.id] = True
    await message.answer("✅ Уведомления активированы на 30 дней!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
