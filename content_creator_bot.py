import os
from threading import Thread
from flask import Flask

app = Flask('')

@app.route('/')
def home():
    return "Bot is active!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
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
ai_client = genai.GenerativeModel('gemini-3.6-flash')

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
post_to_facebook_and_instagram(news_text)

async def main():
    print("🚀 የቴሌግራም ቦት በ Render.com ላይ ስራ ጀምሯል...")
    while True:
        await fetch_and_post()
        print("⏰ የሚቀጥለው ዜና ከ2 ሰዓት በኋላ ይለካል...")
        # በየ 2 ሰዓቱ (7200 ሰከንድ) እንዲልክ ማድረግ
        await asyncio.sleep(7200)

if __name__ == "__main__":
    asyncio.run(main())
import os
import requests

# Environment variables
FB_PAGE_ID = os.getenv("FB_PAGE_ID", "61593729614740")
FB_DTSG = os.getenv("FB_DTSG")
FB_JAZOEST = os.getenv("FB_JAZOEST")

def post_to_facebook_and_instagram(text_message):
    """
    Posts content directly to Facebook Page and linked Instagram using Session Headers
    """
    url = f"https://www.facebook.com/api/graphql/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    
    payload = {
        "fb_dtsg": FB_DTSG,
        "jazoest": FB_JAZOEST,
        "av": FB_PAGE_ID,
        "__user": FB_PAGE_ID,
        "variables": f'{{"input":{{"actor_id":"{FB_PAGE_ID}","message":{{"text":"{text_message}"}},"client_mutation_id":"1"}}}}',
        "doc_id": "6022321287884803"  # Standard Post Mutation ID
    }
    
    try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            print("[+] Successfully posted to Facebook & Instagram!")
        else:
            print(f"[-] Facebook Post Failed: {response.status_code}")
    except Exception as e:
        print(f"[-] Exception during FB posting: {e}")

# የቴሌግራም ቦትህ ዜና አመንጭቶ ሲጨርስ ይህንን በመጥራት አብሮ እንዲለቅ አድርገው:
# post_to_facebook_and_instagram(generated_news_text)
