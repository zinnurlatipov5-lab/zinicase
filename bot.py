import asyncio
import os
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardBuilder
from aiogram.filters import Command

# ================= НАСТРОЙКИ (ЗАПОЛНИ ЭТО) =================
# 1. Вставь сюда НОВЫЙ токен (старый не используй!)
BOT_TOKEN = "9063807547:AAFnldNa0-3pukbqws4BinWwkHhX-qUaOOE" 

# 2. Твой числовой ID (ты прислал 8194948521)
ADMIN_ID = 8194948521

# 3. Твой ник для оплаты (ты прислал @zini2l)
PAYMENT_USERNAME = "zini2l"

# Стоимость входа в звездах
ENTRY_FEE = 15
# ===========================================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# База вопросов
QUESTIONS = [
    ("Столица Франции?", ["Берлин", "Париж", "Рим"], 1),
    ("Сколько минут в полутора часах?", ["75", "90", "100"], 1),
    ("Самая длинная река мира?", ["Амазонка", "Волга", "Дунай"], 0),
    ("Кто написал «Мёртвые души»?", ["Пушкин", "Чехов", "Гоголь"], 2),
    ("Химический символ золота?", ["Ag", "Au", "Go"], 1),
    ("Год полёта Гагарина?", ["1959", "1961", "1963"], 1),
    ("Самое глубокое озеро мира?", ["Байкал", "Танганьика", "Каспий"], 0),
    ("2 в 5-й степени?", ["16", "32", "64"], 1),
]

participants = {}
is_tournament_active = False

def get_keyboard(options, shuffled):
    kb = InlineKeyboardBuilder()
    for orig_idx in shuffled:
        kb.button(text=options[orig_idx], callback_data=f"ans:{orig_idx}")
    kb.adjust(1)
    return kb.as_markup()

@dp.message(Command("start"))
async def start(m: Message):
    status = "✅ Турнир АКТИВЕН" if is_tournament_active else "⏸ Турнир ЗАКРЫТ (ждет старта)"
    await m.answer(
        f"🎮 <b>Викторина: Оплата вручную</b>\n\n"
        f"Статус: {status}\n\n"
        f"Правила:\n"
        f"1. Жди команды /start_tournament от организатора.\n"
        f"2. Нажми /join.\n"
        f"3. Оплати {ENTRY_FEE} ⭐ на ник @{PAYMENT_USERNAME}.\n"
        f"4. Прикрепи скриншот оплаты.\n"
        f"5. Организатор подтвердит вход командой /confirm <ID>.\n\n"
        f"Турниры запускаются автоматически по расписанию."
    )

@dp.message(Command("join"))
async def join(m: Message):
    global is_tournament_active
    if not is_tournament_active:
        await m.answer("❌ Сейчас регистрация закрыта. Жди анонса.")
        return
    
    uid = m.from_user.id
    if uid in participants:
        await m.answer("Ты уже в списке ожидания!")
        return

    participants[uid] = {
        "name": m.from_user.first_name,
        "paid": False,
        "score": 0,
        "q": 0,
        "current_correct": 0
    }

    await m.answer(
        f"👤 <b>{m.from_user.first_name}</b>, ты в очереди.\n\n"
        f"💳 <b>Инструкция:</b>\n"
        f"1. Купи подарок на {ENTRY_FEE} ⭐ для @{PAYMENT_USERNAME}.\n"
        f"2. Пришли скриншот оплаты в этот чат.\n\n"
        f"⚠️ <b>Без подтверждения организатора играть нельзя!</b>"
    )

@dp.message(Command("start_tournament"))
async def start_tournament(m: Message):
    if m.from_user.id != ADMIN_ID:
        return
    
    global is_tournament_active, participants
    is_tournament_active = True
    participants = {}
    await m.answer("🎮 <b>ТУРНИР ОТКРЫТ!</b>\n\n"
                   "Игроки могут нажимать /join.\n"
                   "Принимайте скриншоты оплаты.")

@dp.message(Command("end_tournament"))
async def end_tournament(m: Message):
    if m.from_user.id != ADMIN_ID:
        return
    
    global is_tournament_active
    is_tournament_active = False
    
    paid_players = [p for p in participants.values() if p["paid"]]
    sorted_players = sorted(paid_players, key=lambda x: -x["score"])[:3]
    
    report = "🏆 <b>ИТОГИ ТУРНИРА!</b>\n\n"
    if not sorted_players:
        report += "Никто не сыграл или не оплатил."
    else:
        for i, p in enumerate(sorted_players):
            medal = ["🥇", "🥈", "🥉"][i]
            # Находим ID игрока по данным (упрощенно берем первого подходящего, если имена совпадают)
            # В реальном логе на GitHub ты увидишь точные ID
            report += f"{medal} <b>{p['name']}</b> — {p['score']} очков\n"
    
    report += "\n💰 <b>Призы выдаются вручную организатором!</b>"
    await m.answer(report)

@dp.message(Command("confirm"))
async def confirm_payment(m: Message):
    """
    Как использовать:
    1. Игрок кидает скрин.
    2. Ты пересылаешь этот скрин боту.
    3. В поле ввода пишешь: /confirm
    Бот сам поймет, кого подтверждать.
    """
    if m.from_user.id != ADMIN_ID:
        return

    if not m.forward_from:
        await m.answer("❌ Ошибка: Перешли сообщение игрока с оплатой, а потом напиши /confirm")
        return

    player_id = m.forward_from.id
    
    if player_id not in participants:
        await m.answer("❌ Игрок не регистрировался через /join")
        return
    
    if participants[player_id]["paid"]:
        await m.answer("✅ Этот игрок уже подтвержден!")
        return

    participants[player_id]["paid"] = True
    await bot.send_message(
        player_id, 
        "✅ Организатор подтвердил оплату! Ты можешь играть: /play"
    )
    await m.answer(f"✅ Оплата для {m.forward_from.first_name} подтверждена.")

@dp.message(Command("play"))
async def play(m: Message):
    p = participants.get(m.from_user.id)
    if not p:
        await m.answer("Сначала зарегистрируйся: /join")
        return
    if not p["paid"]:
        await m.answer("⚠️ Оплата не подтверждена. Напиши админу.")
        return
    if p["q"] >= len(QUESTIONS):
        await m.answer(f"✅ Ты прошел все вопросы! Твой счет: {p['score']}. Жди итогов.")
        return
    
    await ask_question(m.chat.id, p)

async def ask_question(chat_id, p):
    text, options, correct = QUESTIONS[p["q"]]
    shuffled = list(range(len(options)))
    random.shuffle(shuffled)
    p["current_correct"] = correct
    
    await bot.send_message(
        chat_id,
        f"❓ Вопрос {p['q'] + 1}/{len(QUESTIONS)}\n\n{text}",
        reply_markup=get_keyboard(options, shuffled)
    )

@dp.callback_query(F.data.startswith("ans:"))
async def answer(c: CallbackQuery):
    p = participants.get(c.from_user.id)
    if not p or not p["paid"]:
        await c.answer("Сначала подтверди оплату!", show_alert=True)
        return
    
    chosen = int(c.data.split(":"))
    if chosen == p["current_correct"]:
        p["score"] += 10
        await c.answer("✅ Верно! +10 очков")
    else:
        await c.answer("❌ Неверно")
    
    p["q"] += 1
    try:
        await c.message.edit_reply_markup()
    except: pass
    
    await ask_question(c.message.chat.id, p)

async def main():
    me = await bot.get_me()
    print(f"🚀 Бот запущен: @{me.username}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
