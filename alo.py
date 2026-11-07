import os
from threading import Thread
from flask import Flask


app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()



import time
import telebot

TOKEN = "9229808034:AAFQESmcmnWNLn58qT-st_ob2J9G9Hqz5aI"
ADMIN_CHAT_ID = 6028565929

telebot.apihelper.CONNECT_TIMEOUT = 20
telebot.apihelper.READ_TIMEOUT = 60

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
  user_name = message.from_user.first_name
  bot.reply_to(
      message,
      f"هلا حبيب قلبي {user_name}, نورت! 🌹\nاكتب رسالتك وسأقوم بتوصيلها إلى"
      " المطور مباشرة.",
  )
  bot.send_message(
      ADMIN_CHAT_ID,
      f"🚨 تنبيه: شخص جديد دخل البوت!\n👤 الاسم: {user_name}\n🆔 الآيدي:"
      f" {message.from_user.id}",
      parse_mode="Markdown",
  )


@bot.message_handler(func=lambda message: True)
def forward_to_admin(message):
  user_id = message.from_user.id
  full_name = message.from_user.first_name
  username = (
      f"@{message.from_user.username}"
      if message.from_user.username
      else "بدون معرف"
  )

  text_to_send = (
      f"📩 رسالة جديدة من: {full_name} ({username})\n"
      f"🆔 الآيدي: {user_id}\n\n"
      f"الرسالة: {message.text}"
  )

  bot.send_message(ADMIN_CHAT_ID, text_to_send, parse_mode="Markdown")
  bot.reply_to(
      message, "✅ وصلت رسالتك حبيبي، سيتم الرد عليك في أقرب وقت."
  )


print("Bot is running and listening...")

while True:
  try:
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
  except Exception as e:
    print(
        f"صار انقطاع بالاتصال، جارٍ إعادة المحاولة خلال 5 ثوانٍ... الخطأ: {e}"
    )
    time.sleep(5)
