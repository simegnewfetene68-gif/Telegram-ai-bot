import os
import re
from gtts import gTTS
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-3.6-flash')

def generate_tiktok_content(topic, mood):
    prompt = f"""
ለ TikTok/Reels የሚሆን አጭር ቫይራል ስክሪፕት አዘጋጅ።

ርዕስ: {topic}
ስሜት: {mood}

መልስህን በዚህ ቅርፅ ብቻ ስጥ:
[VOICEOVER]
እዚህ ጋር ተናጋሪው የሚናገረው ንጹህ የአማርኛ ጽሁፍ ብቻ ይፃፍ። ምንም ምልክት ወይም ቅንፍ አታስገባ።
[END_VOICEOVER]

[PROMPT]
እዚህ ጋር ለ AI Image Generator የሚሆን 1 አጭር የቪዲዮ ምስል መግለጫ በእንግሊዝኛ ይፃፍ።
[END_PROMPT]
"""
    response = model.generate_content(prompt)
    return response.text

def text_to_audio(amharic_text, filename="voiceover.mp3"):
    # የአማርኛ ድምፅ ማመንጨት
    tts = gTTS(text=amharic_text, lang='am')
    tts.save(filename)
    print(f"🔊 የድምፅ ፋይል ተዘጋጅቷል: {filename}")

if __name__ == "__main__":
    trend = "በከተማው ውስጥ የወታደራዊ አፈሳ እና የሰዎች መሸሽ አጋጣሚ"
    mood = "አስቂኝ እና ገራሚ"

    print("🎬 የ TikTok ይዘት እና ድምፅ በመዘጋጀት ላይ ነው...")
    raw_content = generate_tiktok_content(trend, mood)
    
    # Voiceover ጽሁፉን ለይቶ ማውጣት
    voiceover_match = re.search(r'\[VOICEOVER\](.*?)\[END_VOICEOVER\]', raw_content, re.DOTALL)
    
    if voiceover_match:
        voice_text = voiceover_match.group(1).strip()
        print("\n--- የተፈጠረው የድምፅ ጽሁፍ ---")
        print(voice_text)
        
        # ድምፅ ወደ mp3 ፋይል መቀየር
        text_to_audio(voice_text)
    else:
        print("የድምፅ ጽሁፉን መለየት አልተቻለም፣ ድጋሚ ይሞክሩ።")
