import logging
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from content_creator_bot import fetch_and_post
from threading import Thread
from dotenv import load_dotenv
from flask import Flask
import google.generativeai as genai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ---------------------------------------------------------
# 1. FLASK WEB SERVER (ለ Render Free Web Service)
# ---------------------------------------------------------
app = Flask('')


@app.route('/')
def home():
  return 'Bot is alive and running!'


def run():
  # Render አውቶማቲክ የሚሰጠውን PORT ይጠቀማል
  port = int(os.environ.get('PORT', 8080))
  app.run(host='0.0.0.0', port=port)


def keep_alive():
  t = Thread(target=run)
  t.start()


# ---------------------------------------------------------
# 2. CONFIGURATION & SETUP
# ---------------------------------------------------------
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not TELEGRAM_BOT_TOKEN or not GEMINI_API_KEY:
  raise ValueError(
      'እባክዎን TELEGRAM_BOT_TOKEN እና GEMINI_API_KEY በ Environment Variables ውስጥ'
      ' መኖራቸውን ያረጋግጡ!'
  )

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3.6-flash')

# ---------------------------------------------------------
# 3. TELEGRAM BOT HANDLERS
# ---------------------------------------------------------


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  welcome_text = (
      'ሰላም! እንኳን ወደ ደንበኞች አገልግሎት ቦት በሰላም መጡ።\n'
      'ምን እንድረዳዎ ይፈልጋሉ? ጥያቄዎን ማስገባት ይችላሉ።'
  )
  await update.message.reply_text(welcome_text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_text = update.message.text
  await update.message.chat.send_action(action='typing')

  try:
    # ለደንበኞች አገልግሎት የሚሆን Prompt አዘጋጅተን ለ Gemini እንልካለን
    system_prompt = (
        'You are a helpful, friendly, and professional customer support assistant.'
        ' Answer the customer query concisely and clearly in Amharic unless asked'
        f' otherwise:\n{user_text}'
    )

    response = model.generate_content(system_prompt)
    await update.message.reply_text(response.text)
  except Exception as e:
    logging.error(f'Error generating AI response: {e}')
    await update.message.reply_text(
        'ይቅርታ፣ ጥያቄዎን በማቀናበር ላይ ሳለን ስህተት አጋጥሟል። እባክዎን ጥቂት ቆይተው እንደገና ይሞክሩ።'
    )


# ---------------------------------------------------------
# 4. MAIN EXECUTION
# ---------------------------------------------------------
async def main():
    # Flask ሰርቨሩን ማስነሳት (ለ Render Health Check)
    keep_alive()

    # የ Scheduler (የሰዓት ቆጣሪ) ማቀናበሪያ
    scheduler = AsyncIOScheduler()
    scheduler.add_job(fetch_and_post, 'interval', hours=2)
    scheduler.start()

    # Telegram Bot ማዘጋጀት
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # ቦቱን ማስነሳት (ለ Support Bot እና ለ Scheduler አብሮ ይሰራል)
    async with application:
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        print("ሁለቱም ቦቶች በ Render ላይ 24/7 ስራ ጀምረዋል...")
        await asyncio.Event().wait()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
