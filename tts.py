import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import threading

# 1. 초기 설정 및 전역 객체 생성
recognizer = sr.Recognizer()

def speak_text(text):
    """텍스트를 음성(TTS)으로 변환하고 재생하는 함수"""
    try:
        tts = gTTS(text=text, lang='ko')
        filename = "temp_voice.mp3"
        tts.save(filename)

        # pygame을 사용하여 mp3 재생
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        # 재생이 끝날 때까지 대기
        while pygame.mixer.music.get_busy():
            pass
        
        pygame.mixer.quit()
        os.remove(filename)  # 재생 후 임시 파일 삭제
    except Exception as e:
        print(f"TTS 오류: {e}")

def start_recording():
    """버튼을 눌렀을 때 실행되는 음성 녹음 및 STT 함수"""
    # UI가 멈추지 않도록 별도의 쓰레드에서 실행
    def record_process():
        with sr.Microphone() as source:
            status_label.config(text="🎙️ 녹음 중... 말씀하세요!", fg="red")
            root.update() # 화면 강제 업데이트
            
            try:
                # 주변 소음 적응 후 5초간 음성 수집
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                status_label.config(text="🔍 분석 중...", fg="blue")
                root.update()

                # 2. 구글 STT로 변환
                text = recognizer.recognize_google(audio_data, language='ko-KR')
                
                # 결과 화면 출력
                result_text.set(text)
                status_label.config(text="✅ 완료!", fg="green")
                
                # 3. 변환된 텍스트를 다시 말하기 (TTS)
                speak_text(text)
                
            except sr.UnknownValueError:
                status_label.config(text="❓ 인식을 못했습니다.", fg="orange")
            except sr.RequestError:
                status_label.config(text="🌐 인터넷 연결을 확인하세요.", fg="orange")
            except Exception as e:
                status_label.config(text=f"⚠️ 오류: {e}", fg="orange")

    threading.Thread(target=record_process).start()

# --- GUI 화면 구성 ---
root = tk.Tk()
root.title("음성 인식 & 말하기 프로그램")
root.geometry("400x300")

# 제목 라벨
tk.Label(root, text="음성 인식 시스템", font=("맑은 고딕", 16, "bold")).pack(pady=10)

# 결과 표시 변수 및 위젯
result_text = tk.StringVar()
result_text.set("결과가 여기에 표시됩니다.")
label_result = tk.Label(root, textvariable=result_text, wraplength=350, font=("맑은 고딕", 12))
label_result.pack(pady=20)

# 상태 표시 라벨 (녹음 중/분석 중 등)
status_label = tk.Label(root, text="대기 중", font=("맑은 고딕", 10))
status_label.pack()

# 녹음 시작 버튼 (재생 버튼 역할)
btn_record = tk.Button(root, text="🔴 녹음 시작 (말하기)", command=start_recording, 
                       width=20, height=2, bg="lightgray", font=("맑은 고딕", 12))
btn_record.pack(pady=20)

root.mainloop()