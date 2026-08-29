import os
import asyncio
import feedparser
from dotenv import load_dotenv
from telegram import Bot
from telegram.request import HTTPXRequest
import google.generativeai as genai
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# .env ፋይል ማነብ
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Gemini ኤፒአይ ማዘጋጀት
genai.configure(api_key=GEMINI_API_KEY)
ai_client = genai.GenerativeModel('gemini-3.6-flash')

# Telegram Bot ከ 60 ሰከንድ Timeout ማስተካከያ ጋር ማዘጋጀት
request_config = HTTPXRequest(connect_timeout=60.0, read_timeout=60.0)
bot = Bot(token=TELEGRAM_BOT_TOKEN, request=request_config)

RSS_URL = "https://news.ycombinator.com/rss"

async def fetch_and_post():
    print("አዲስ ዜና በመፈለግ ላይ ነው...")
    feed = feedparser.parse(RSS_URL)
    
    if not feed.entries:
        print(" ምንም አዲስ ዜና አልተገኘም")
        return

    latest_entry = feed.entries[0]
    title = latest_entry.title
    link = latest_entry.link

    # f-string እና ትክክለኛ የ Gemini ሞዴል ጥሪ
    prompt = f"""
አጭርና ማራኪ የቴሌግራም ፖስት በአማርኛ አዘጋጅ። ቴክኖሎጂያዊ ይዘት ያለው ይሁን።

ርዕስ: {title}
ሊንክ: {link}
"""

    try:
        response = ai_client.generate_content(prompt)
        post_content = f"{response.text}\n\n[ምንጭ]({link})"

        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=post_content,
            parse_mode="Markdown"
        )
        print("ፖስቱ ወደ ቻናሉ በትክክል ተልኳል!")
    except Exception as e:
        print(f"ስህተት አጋጥሟል: {e}")

async def main():
    # ቦቱ ሲነሳ ወዲያውኑ አንዴ ፖስት እንዲያደርግ
    await fetch_and_post()

    # በየ 2 ሰዓቱ አውቶማቲክ ፖስት የሚያደርግ Scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(fetch_and_post, 'interval', hours=2)
    scheduler.start()

    print("Content Creator Bot እየሰራ ነው...")
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
async def main():
    scheduler = AsyncIOScheduler()
    # በየ 2 ሰዓቱ fetch_and_post እንዲሰራ ማዘዝ
    scheduler.add_job(fetch_and_post, 'interval', hours=2)
    scheduler.start()
    
    # ቦቱ Render ላይ ሲጀምር የመጀመሪያውን ዜና ወዲያው እንዲልክ
    await fetch_and_post()
    
    print("🚀 ቦቱ Render.com ላይ በየ 2 ሰዓቱ መስራት ጀምሯል...")
    
    # 24/7 እንዳይቆም የሚያስችል ማለቂያ የሌለው loop
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
