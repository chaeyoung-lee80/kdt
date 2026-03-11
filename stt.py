import os
import speech_recognition as sr


recognizer = sr.Recognizer()
audio_file = './vad_recorded.wav'

# 파일 존재 여부 먼저 확인
if not os.path.exists(audio_file):
    print(f"오류: '{audio_file}' 파일을 찾을 수 없습니다.")
else:
    with sr.AudioFile(audio_file) as source:
        print("음성 파일을 읽는 중...")
        audio_data = recognizer.record(source)

    try:
        # language 설정을 'ko-KR'로 명시
        text = recognizer.recognize_google(audio_data, language='ko-KR')
        print("변환된 텍스트: ", text)
    except sr.UnknownValueError:
        print("음성을 이해할 수 없습니다. (인식 실패)")
    except sr.RequestError as e:
        print(f"Google 서비스에 접근할 수 없습니다; {e}")
    except Exception as e:
        print(f"기타 오류 발생: {e}")

        