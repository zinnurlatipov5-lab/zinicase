import asyncio
import os
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, LabeledPrice
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

BOT_TOKEN = os.environ["BOT_TOKEN"]
ENTRY_FEE = 15           # звёзд за участие
POOL_SHARE = 0.8         # 80% депозитов — призовой фонд
SPLIT = [0.5, 0.3, 0.2]  # доли 1-го, 2-го и 3-го места

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

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

participants = {}  # user_id -> данные игрока
deposits = 0       # сумма всех взносов


def keyboard(options, shuffled):
    kb = InlineKeyboardBuilder()
    for orig_idx in shuffled:
        kb.button(text=options[orig_idx], callback_data=f"ans:{orig_idx}")
    kb.adjust(1)
    return kb.as_markup()


@dp.message(Command("start"))
async def start(m: Message):
    await m.answer(
        "🏆 <b>Турнир-викторина</b>\n\n"
        f"Вход: <b>{ENTRY_FEE} ⭐</b>\n"
        "Топ-3 по очкам делят 80% всех взносов: 50/30/20%.\n\n"
        "Участвовать: /join\nИграть: /play\nРейтинг: /top"
    )


@dp.message(Command("join"))
async def join(m: Message):
    uid = m.from_user.id
    if uid in participants:
        await m.answer("Ты уже участвуешь. Играй: /play")
        return
    await bot.send_invoice(
        chat_id=m.chat.id,
        title="Участие в турнире",
        description="Вход в викторину. Призовой фонд — 80% всех взносов.",
        payload=f"entry_{uid}",
        currency="XTR",
        prices=[LabeledPrice(label="Вход", amount=ENTRY_FEE)],
    )


@dp.message(F.successful_payment)
async def paid(m: Message):
    global deposits
    uid = m.from_user.id
    participants[uid] = {
        "user_id": uid,
        "name": m.from_user.first_name or "Игрок",
        "chat_id": m.chat.id,
        "payment_id": m.successful_payment.telegram_payment_charge_id,
        "score": 0,
        "q": 0,
        "current_correct": 0,
    }
    deposits += ENTRY_FEE
    await m.answer(
        f"✅ Оплата прошла, ты в игре!\n"
        f"Участников: {len(participants)} | Фонд: {int(deposits * POOL_SHARE)} ⭐\n\n"
        "Начинаем: /play"
    )


@dp.message(Command("play"))
async def play(m: Message):
    p = participants.get(m.from_user.id)
    if not p:
        await m.answer("Сначала оплати участие: /join")
        return
    await ask_question(m.chat.id, p)


async def ask_question(chat_id, p):
    if p["q"] >= len(QUESTIONS):
        await bot.send_message(chat_id,
            f"Ты ответил на все вопросы! Счёт: {p['score']}.\n"
            "Итоги подведёт организатор командой /end.")
        return
    text, options, correct = QUESTIONS[p["q"]]
    shuffled = list(range(len(options)))
    random.shuffle(shuffled)
    p["current_correct"] = correct
    await bot.send_message(
        chat_id,
        f"Вопрос {p['q'] + 1}/{len(QUESTIONS)}.\n{text}",
        reply_markup=keyboard(options, shuffled),
    )


@dp.callback_query(F.data.startswith("ans:"))
async def answer(c: CallbackQuery):
    p = participants.get(c.from_user.id)
    if not p:
        await c.answer("Сначала оплати участие: /join", show_alert=True)
        return
    chosen = int(c.data.split(":")[1])
    if chosen == p["current_correct"]:
        p["score"] += 10
        await c.answer("✅ Верно! +10")
    else:
        await c.answer("❌ Мимо")
    p["q"] += 1
    try:
        await c.message.edit_reply_markup()
    except Exception:
        pass
    await ask_question(c.message.chat.id, p)


def top_list():
    return sorted(participants.values(), key=lambda x: -x["score"])[:3]


@dp.message(Command("top"))
async def top(m: Message):
    pool = int(deposits * POOL_SHARE)
    lines = [f"Участников: {len(participants)} | Фонд: {pool} ⭐\n"]
    for i, p in enumerate(sorted(participants.values(), key=lambda x: -x["score"])[:10]):
        medal = "🥇🥈🥉"[i] if i < 3 else f"{i+1}."
        lines.append(f"{medal} {p['name']} — {p['score']}")
    await m.answer("\n".join(lines))


async def finish(chat_id):
    if not participants:
        await bot.send_message(chat_id, "Участников пока нет.")
        return
    pool = int(deposits * POOL_SHARE)
    prizes = [int(pool * s) for s in SPLIT]
    lines = ["🏁 <b>Итоги турнира</b>\n"]
    for i, w in enumerate(top_list()):
        lines.append(f"{i+1}. {w['name']} — {w['score']} очков → {prizes[i]} ⭐")
    await bot.send_message(chat_id, "\n".join(lines))

    # возврат взноса победителям — максимум, что разрешает Telegram
    for i, w in enumerate(top_list()):
        try:
            await bot.refund_star_payment(
                user_id=w["user_id"],
                telegram_payment_charge_id=w["payment_id"],
            )
            await bot.send_message(w["chat_id"],
                f"🎉 Ты в топ-3 (место {i+1})! Взнос {ENTRY_FEE} ⭐ возвращён.")
        except Exception:
            await bot.send_message(w["chat_id"],
                f"🎉 Ты в топ-3 (место {i+1})! Напиши организатору за призом.")

    participants.clear()
    globals()["deposits"] = 0


@dp.message(Command("end"))
async def end(m: Message):
    await finish(m.chat.id)


async def main():
    me = await bot.get_me()
    print("Бот запущен:", me.username)
    await dp.start_polling(bot)

asyncio.run(main())
