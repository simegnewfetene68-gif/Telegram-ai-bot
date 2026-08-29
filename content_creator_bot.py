import os
import asyncio
import feedparser
import google.generativeai as genai
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Gemini configuration
genai.configure(api_key=GEMINI_API_KEY)
ai_client = genai.GenerativeModel('gemini-1.5-flash')

# Telegram Bot configuration
bot = Bot(token=TELEGRAM_BOT_TOKEN)

RSS_URL = "https://news.ycombinator.com/rss"

async def fetch_and_post():
    try:
        print("🔍 አዲስ ዜና በመፈለግ ላይ ነው...")
        feed = feedparser.parse(RSS_URL)
        
        if not feed.entries:
            print("❌ ምንም አዲስ ዜና አልተገኘም")
            return

        latest_entry = feed.entries[0]
        title = latest_entry.title
        link = latest_entry.link

        prompt = f"""
እባክህ የሚከተለውን የቴክኖሎጂ ዜና በአማርኛ አጭርና ማራኪ አድርገህ አዘጋጅ፡

ርዕስ: {title}
ሊንክ: {link}
"""
        response = ai_client.generate_content(prompt)
        post_content = f"{response.text}\n\nምንጭ፡ {link}"

        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=post_content
        )
        print("✅ ዜናው በቴሌግራም ላይ በጥሩ ሁኔታ ተለቋል!")

    except Exception as e:
        print(f"⚠️ ስህተት ተፈጠረ፦ {e}")

async def main():
    print("🚀 የቴሌግራም ቦት በ Render.com ላይ ስራ ጀምሯል...")
    while True:
        await fetch_and_post()
        print("⏰ የሚቀጥለው ዜና ከ2 ሰዓት በኋላ ይለካል...")
        # በየ 2 ሰዓቱ (7200 ሰከንድ) እንዲልክ ማድረግ
        await asyncio.sleep(7200)

if __name__ == "__main__":
    asyncio.run(main())
