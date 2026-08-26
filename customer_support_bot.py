import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

ai_client = genai.Client(api_key=GEMINI_API_KEY)

# የንግድ ድርጅቱ መረጃ (System Prompt) - የራስህን አገልግሎቶች እና ዋጋ እዚህ መቀየር ትችላለህ
BUSINESS_CONTEXT = """
እርስዎ የ'Tech & Cyber Solutions' የደንበኞች አገልግሎት AI ረዳት ነዎት።
የድርጅቱ ዋና ዋና አገልግሎቶች እና ዋጋዎች፦
1. የዌብሳይት ደህንነት ፍተሻ (Vulnerability Audit) - 8,000 ብር
2. የቴሌግራም AI ቦት ማበልፀግ (Bot Development) - 5,000 ብር
3. የኔትወርክ ውቅረት እና ደህንነት (Network Setup) - 10,000 ብር

ደንበኞች ስለ አገልግሎቶቹ፣ ዋጋዎች ወይም አሰራር ሲጠይቁ ሁልጊዜ በትህትና፣ በአጭሩ እና በማብራራት በአማርኛ ይመልሱ።
ስለ ድርጅቱ ያልሆነ ጥያቄ ሲጠየቁ 'እኔ የTech & Cyber Solutions ረዳት ስለሆንኩ ከዚሁ ጋር በተያያዘ ልረዳዎ እችላለሁ' ብለው ይመልሱ።
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "ሰላም! እንኳን ወደ Tech & Cyber Solutions የደንበኞች አገልግሎት በደህና መጡ።\n\n"
        "ስለ አገልግሎቶቻችን፣ ዋጋዎች ወይም የቴክኖሎጂ ጥያቄዎች ካሉዎት መጠየቅ ይችላሉ!"
    )
    await update.message.reply_text(welcome_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    print(f"የመጣ ጥያቄ: {user_text}")

    prompt = f"{BUSINESS_CONTEXT}\n\nየደንበኛ ጥያቄ: {user_text}"

    response = ai_client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    await update.message.reply_text(response.text)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Customer Support Bot እየሰራ ነው...")
    app.run_polling()
