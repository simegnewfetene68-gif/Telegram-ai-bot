import os
import re
import urllib.parse
import asyncio
import requests
import edge_tts
import google.generativeai as genai
from moviepy import AudioFileClip, ImageClip
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-3.6-flash')

def get_boxing_dialogue(topic, mood):
    prompt = f"""
ለ TikTok የሚሆን አጭርና በጣም አስቂኝ የሁለት ስፖርተኛ ወንድ ጓደኛሞች (ነጭ በግ እና ነጭ ድመት) ውይይት አዘጋጅ።
ርዕስ: {topic} | ስሜት: {mood}

ህጎች፦
1. ውይይቱ ሙሉ በሙሉ ስለ ሴዶን (Cédon) የትናንቱ የቦክስ/ፋይቲንግ (Boxing/Fighting) ሽንፈት እና በቡጢ መመታት የሚያሽሟጥጥ ይሁን!
2. "በግ አለ" ወይም "ድመት አለ" የሚል መግለጫ ጽሁፍ በፍፁም እንዳይኖር!
3. ጽሁፉ ቀጥታ በሁለቱ ወንድ ስፖርተኞች መካከል የሚደረግ የተቀባበለ ንግግር ብቻ ይሁን።

መልስህን በዚህ ቅርፅ ብቻ ስጥ:
[SHEEP_VOICE]
እዚህ ጋር ስፖርተኛው ነጭ በግ ስለ ሴዶን የቦክስ ሽንፈት የሚያሽሟጥጠው አስቂኝ ንግግር።
[END_SHEEP]

[CAT_VOICE]
እዚህ ጋር ሌላኛው ስፖርተኛ ነጭ ድመት የሚያሽሟጥጠው አስቂኝ ንግግር።
[END_CAT]

[IMAGE_PROMPT]
Full body 3D Pixar style character render of two handsome athletic male best friends standing in a luxury gym: on the LEFT, a strong male white sheep with distinct curved ram horns and white wool texture. On the RIGHT, a cute white male cat with pointy ears and whiskers. Both wearing colorful stylish modern gym sportswear, highly detailed 8k resolution, photorealistic 3D character design
[END_IMAGE_PROMPT]
"""
    res = model.generate_content(prompt)
    text = res.text
    
    sheep_text = re.search(r'\[SHEEP_VOICE\](.*?)\[END_SHEEP\]', text, re.DOTALL).group(1).strip()
    cat_text = re.search(r'\[CAT_VOICE\](.*?)\[END_CAT\]', text, re.DOTALL).group(1).strip()
    img_prompt = re.search(r'\[IMAGE_PROMPT\](.*?)\[END_IMAGE_PROMPT\]', text, re.DOTALL).group(1).strip()
    
    return sheep_text, cat_text, img_prompt

def download_hd_image(prompt, output_path="scene.jpg"):
    print("🎨 ነጭ በግ እና ነጭ ድመትን የሚለይ ጥራት ያለው HD ምስል በማፍለቅ ላይ ነው...")
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&seed=999&model=flux&nologo=true"
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"🖼️ HD ምስል ተወርዷል: {output_path}")
        return True
    return False

async def generate_voice(text, voice_name, output_file):
    communicate = edge_tts.Communicate(text, voice_name)
    await communicate.save(output_file)

def make_final_video(trend, mood):
    print("📝 ስክሪፕቱን በማዘጋጀት ላይ ነው...")
    s_text, c_text, img_prompt = get_boxing_dialogue(trend, mood)
    
    print(f"\n🏋️‍♂️ ነጭ በግ (ወንድ ድምፅ 1): {s_text}")
    print(f"🏋️‍♂️ ነጭ ድመት (ወንድ ድምፅ 2): {c_text}\n")
    
    print("🔊 የሁለቱን ወንዶች ድምፅ በማዘጋጀት ላይ ነው...")
    asyncio.run(generate_voice(s_text, "am-ET-AmehaNeural", "voice1.mp3"))
    asyncio.run(generate_voice(c_text, "am-ET-AmehaNeural", "voice2.mp3"))
    
    os.system("ffmpeg -y -i voice1.mp3 -i voice2.mp3 -filter_complex '[0:a][1:a]concat=n=2:v=0:a=1[a]' -map '[a]' audio.mp3 > /dev/null 2>&1")
    
    download_hd_image(img_prompt, "scene.jpg")
    
    print("🎬 ቪዲዮውን ያለ ምንም መንቀጥቀጥ በጠራ ጥራት በማዋሃድ ላይ ነው...")
    audio_clip = AudioFileClip("audio.mp3")
    
    # መንቀጥቀጡን ለማስቀረት static image clip ብቻ እንጠቀማለን
    image_clip = ImageClip("scene.jpg").with_duration(audio_clip.duration)
    
    video = image_clip.with_audio(audio_clip)
    
    output_video = "tiktok_viral_output.mp4"
    # libx264 በመጠቀም መንቀጥቀጥ የሌለው ጥራት ያለው ቪዲዮ ማውጣት
    video.write_videofile(output_video, fps=24, codec="libx264", audio_codec="aac")
    
    audio_clip.close()
    image_clip.close()
    video.close()
    
    print(f"\n🚀 አዲሱ የተስተካከለው ቪዲዮ ተዘጋጅቷል: {output_video}")

if __name__ == "__main__":
    current_trend = "የትናንቱ የሴዶን (Cédon) የቦክስ/ፋይቲንግ (Boxing/Fighting) ሽንፈት እና በቡጢ መመታት"
    chosen_mood = "በጣም አስቂኝ እና አሽሙር"
    make_final_video(current_trend, chosen_mood)
