import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import pygame
import os
import time

# 1. 초기 설정
recognizer = sr.Recognizer()
translator = Translator()

def speak_japanese(text):
    """일본어 텍스트를 음성으로 변환하여 재생합니다."""
    tts = gTTS(text=text, lang='ja')
    filename = "result_ja.mp3"
    tts.save(filename)
    
    # pygame을 이용한 오디오 재생
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    
    # 재생이 끝날 때까지 대기
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    
    pygame.mixer.quit()
    os.remove(filename) # 재생 후 임시 파일 삭제

# 2. 음성 인식 시작
with sr.Microphone() as source:
    print("🎤 한국어로 말씀해 주세요...")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    audio = recognizer.listen(source)

try:
    # 3. 한국어 음성을 텍스트로 변환
    korean_text = recognizer.recognize_google(audio, language='ko-KR')
    print(f"🇰🇷 한국어 인식: {korean_text}")

    # 4. 일본어로 번역
    translated = translator.translate(korean_text, src='ko', dest='ja')
    japanese_text = translated.text
    print(f"🇯🇵 일본어 번역: {japanese_text}")

    # 5. 일본어로 말하기
    speak_japanese(japanese_text)

except sr.UnknownValueError:
    print("❌ 음성을 이해하지 못했습니다.")
except Exception as e:
    print(f"⚠️ 오류 발생: {e}")