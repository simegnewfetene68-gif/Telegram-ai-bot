import os
import asyncio
import feedparser
from dotenv import load_dotenv
from telegram import Bot
from google import genai
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")

ai_client = genai.Client(api_key=GEMINI_API_KEY)
bot = Bot(token=TELEGRAM_BOT_TOKEN)

RSS_URL = "https://news.ycombinator.com/rss"

async def fetch_and_post():
    print("አዲስ መረጃ እየተፈለገ ነው...")
    feed = feedparser.parse(RSS_URL)
    
    if not feed.entries:
        print("ምንም አዲስ መረጃ አልተገኘም።")
        return

    latest_entry = feed.entries[0]
    title = latest_entry.title
    link = latest_entry.link

    # የራስህ ሀሳብ እና መመሪያ እዚህ prompt ውስጥ ነው የሚገባው፦
    prompt = f"""
    እባክህን የሚከተለውን የዜና ርዕስ መሰረት በማድረግ ለቴሌግራም ቻናል የሚሆን በአማርኛ የተዘጋጀ አጭር፣ ሳቢ እና አስተማሪ ፖስት አዘጋጅ።

    የራስህ መመሪያዎች፦
    1. ፅሁፉን ስታጠቃልል ሁልጊዜ፦ "ለተጨማሪ አዳዲስ የቴክኖሎጂ መረጃዎች ቻናላችንን ተቀላቀሉ!" የሚል መልእክት ጨምርበት።
    2. አቀራረቡ ሙያዊ እና ለማንበብ ቀላል ይሁን።
    3. ተስማሚ ኢሞጂዎችን እና ሃሽታጎችን አክል።

    ርዕስ፡ {title}
    ምንጭ፡ {link}
    """

    response = ai_client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    post_content = f"{response.text}\n\n🔗 [ሙሉውን ለማንበብ]({link})"

    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=post_content,
        parse_mode="Markdown"
    )
    print("ፖስቱ አውቶማቲክ በቻናል ላይ ተለቅቋል!")

async def main():
    await fetch_and_post()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(fetch_and_post, 'interval', hours=2)
    scheduler.start()
    
    print("Content Creator Bot እየሰራ ነው...")
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
