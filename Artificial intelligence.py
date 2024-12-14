import speech_recognition as sr
import time
from mistralai import Mistral
from gtts import gTTS
import os
import pygame

api_key = "jxCbOuu5NVj200y9yjQEhKt8VKkJ2rGK"
model = "mistral-large-latest"
client = Mistral(api_key=api_key)

def get_mistral_response(user_message):
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": user_message,
            },
        ]
    )
    return chat_response.choices[0].message.content

def speak(text):
    try:
        tts = gTTS(text=text, lang='ru')
        audio_file = "response.mp3"
        tts.save(audio_file)

        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        os.remove(audio_file)
    except Exception as e:
        print(f"Ошибка при воспроизведении звука: {e}")

def listen_and_save():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    print("Говорите что-то (для выхода нажмите Ctrl+C)...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                print("Слушаю...")
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio, language='ru-RU')
                print(f"Вы сказали: {text}")
                user_question = text
                answer = get_mistral_response(user_question)
                print(f"Ответ ИИ: {answer}")

                speak(answer)

                with open("ss.txt", "a", encoding="utf-8") as file:
                    file.write(text + "\n")
                    
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                print("Не удалось распознать речь.")
            except sr.RequestError as e:
                print(f"Ошибка сервиса распознавания: {e}")
            except KeyboardInterrupt:
                print("\nВыход из программы...")
                break

if __name__ == "__main__":
    listen_and_save()
