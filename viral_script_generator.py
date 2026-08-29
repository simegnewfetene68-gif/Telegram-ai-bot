import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-3.6-flash')

def generate_tiktok_script(topic, mood):
    prompt = f"""
እባክህ ለ TikTok/Reels የሚሆን አጭር፣ ቫይራል ሊወጣ የሚችል የቪዲዮ ስክሪፕት አዘጋጅ።

የቪዲዮው ርዕስ/ወቅታዊ ጉዳይ: {topic}
የቪዲዮው ስሜት (Mood): {mood} (ለምሳሌ: አስቂኝ/Satirical, አሳዛኝ, ወይም አስገራሚ)

ስክሪፕቱ የሚከተሉትን ክፍሎች ማካተት አለበት:
1. **Hook (የመጀመሪያዎቹ 3 ሰከንድ):** የተመልካቹን ትኩረት ወዲያውኑ የሚስብ አረፍተ ነገር።
2. **Visual Prompts [በቅንፍ ውስጥ]:** በቪዲዮው ላይ መታየት ያለበት የ AI ምስል ወይም የቪዲዮ መግለጫ።
3. **Voiceover Text:** ተናጋሪው የሚናገረው ተፈጥሯዊና ማራኪ የኢትዮጵያ ሀገር ውስጥ አማርኛ ንግግር።
4. **Call to Action (CTA):** በስተመጨረሻ ላይ ኮሜንት እንዲያደርጉ ወይም ፎሎው እንዲያደርጉ የሚጋብዝ።

ቋንቋው በጣም ዘመናዊ፣ የጎዳና/የህዝብ ወሬ አቀራረብ ያለው እና ሳቢ ይሁን።
"""

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # ለምሳሌ ወቅታዊውን ወታደራዊ አፈሳ በአስቂኝ መልክ መሞከሪያ
    current_trend = "በከተማው ውስጥ የወታደራዊ አፈሳ እና የሰዎች መሸሽ አጋጣሚ"
    chosen_mood = "አስቂኝ እና ገራሚ (Satirical & Funny)"
    
    print("🎬 የ ቫይራል TikTok ስክሪፕት በመዘጋጀት ላይ ነው...\n")
    script = generate_tiktok_script(current_trend, chosen_mood)
    print("--- የተዘጋጀው ስክሪፕት ---\n")
    print(script)
