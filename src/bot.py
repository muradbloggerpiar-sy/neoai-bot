import os
import telebot
from openai import OpenAI
from flask import Flask
import threading

BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
OPENAI_KEY = os.environ.get('OPENAI_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=OPENAI_KEY)

app = Flask(__name__)

@app.route('/')
def health():
    return "Bot is running"

def run_web():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я NeoAI. Напиши мне любой вопрос, и я отвечу.")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, response.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, "Ошибка. Попробуй позже.")

threading.Thread(target=run_web).start()
bot.polling(none_stop=True)
