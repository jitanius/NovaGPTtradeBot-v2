from flask import Flask, request
from telegram import Bot
import os

# ТВОИ КОНСТАНТЫ
BOT_TOKEN = "8071961528:AAH90jXpwKD9CZPKD080mBCmxhY4IuSx7zE"
AUTHORIZED_CHAT_ID = 709004001

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

last_signals = []

@app.route('/', methods=['GET'])
def index():
    return "Final SR Final Edition 3.0 — Телеграм-Бот — СТЕНА УСТАНОВЛЕНА"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    symbol = data.get("symbol", "")
    side = data.get("side", "")
    price = data.get("price", "")
    rsi = data.get("rsi", "")
    sl = data.get("sl", "")
    tp = data.get("tp", "")

    message = (
        f"⚡️ Final SR Final Edition 3.0\n\n"
        f"📈 Инструмент: {symbol}\n"
        f"👉 Сигнал: {side}\n"
        f"💵 Цена: {price}\n"
        f"💡 RSI: {rsi}\n"
        f"🎯 SL: {sl}\n"
        f"🎯 TP: {tp}"
    )
    bot.send_message(chat_id=AUTHORIZED_CHAT_ID, text=message)

    # Сохраняем сигнал
    last_signals.append(message)
    if len(last_signals) > 10:
        last_signals.pop(0)

    return "OK"

@app.route("/commands", methods=["POST"])
def commands():
    data = request.json
    chat_id = data.get("chat_id")
    text = data.get("text", "").lower()

    if str(chat_id) != str(AUTHORIZED_CHAT_ID):
        bot.send_message(chat_id=chat_id, text="❌ Доступ запрещён.")
        return "OK"

    if text == "/status":
        reply = "✅ Final SR Final Edition 3.0 — Текущая ситуация.\nВсе системы работают."
    elif text == "/signals":
        reply = "⚡️ Последние сигналы:\n\n" + '\n'.join(last_signals[-5:]) if last_signals else "Нет сигналов."
    elif text == "/help":
        reply = ("👊 Final SR Final Edition 3.0 — Телеграм-Бот\n"
                 "✅ Команды:\n"
                 "/status — Текущая ситуация\n"
                 "/signals — Последние сигналы\n"
                 "/help — Эта справка\n\n"
                 "GPT. Теперь с тобой.")
    else:
        reply = "❓ Неизвестная команда."

    bot.send_message(chat_id=chat_id, text=reply)
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
