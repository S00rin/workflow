import os
import openai
import requests
from datetime import datetime

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

openai.api_key = OPENAI_API_KEY

def get_mitre_lesson():
    prompt = """
    یکی از تکنیک‌های MITRE ATT&CK را انتخاب کن.
    آن را در کمتر از 150 کلمه به فارسی توضیح بده.
    شامل: توضیح کلی، یک مثال واقعی، و یک روش شناسایی.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

def text_to_speech(text, filename):
    audio_response = openai.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )
    with open(filename, "wb") as f:
        f.write(audio_response)

def send_audio_to_telegram(filename):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendAudio"
    files = {'audio': open(filename, 'rb')}
    data = {'chat_id': CHAT_ID, 'caption': f"آموزش امروز - {datetime.now().strftime('%Y-%m-%d')}"}
    requests.post(url, files=files, data=data)

if __name__ == "__main__":
    lesson = get_mitre_lesson()
    text_to_speech(lesson, "lesson.mp3")
    send_audio_to_telegram("lesson.mp3")
