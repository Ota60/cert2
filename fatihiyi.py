import os
import time
import wave
import threading
from gtts import gTTS
from playsound import playsound
import webbrowser
import speech_recognition as sr

def help():
    speak("Yardım,internete gir,uyku,kapat,selam,çıkış,yazı yazacağım,video izleyeceğim,ilahi aç")
def speak(text):
    audio_path = "response.mp3"

    # Mevcut dosyayı sil (eğer varsa)
    if os.path.exists(audio_path):
        os.remove(audio_path)

    # Yeni dosya oluştur ve sesli yanıtı kaydet
    tts = gTTS(text=text, lang='tr')
    tts.save(audio_path)

    # Dosyayı oynat
    playsound(audio_path)


def save_audio(audio_data, filename="recorded_audio.wav"):
    """Verilen audio verisini .wav dosyasına kaydeder."""
    with wave.open(filename, "wb") as wav_file:
        wav_file.setnchannels(1)  # Mono kanal
        wav_file.setsampwidth(audio_data.sample_width)
        wav_file.setframerate(audio_data.sample_rate)
        wav_file.writeframes(audio_data.frame_data)


def get_audio_input(timeout=None):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Sizi dinliyorum...")
        recognizer.adjust_for_ambient_noise(source)

        try:
            # Ses kaydını al
            audio = recognizer.listen(source, timeout=timeout)
            save_audio(audio)

            # Google Speech Recognition ile sesi metne çevir
            command = recognizer.recognize_google(audio, language='tr-TR')
            return command.lower()

        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("Servis hatası. Lütfen internet bağlantınızı kontrol edin.")
            return ""
        except Exception as e:
            print(f"Bir hata oluştu: {e}")
            return ""


def uyku_modu():
    speak("Uyku moduna geçiyorum. Lütfen süreyi söyleyin.")
    try:
        süre = int(input("Süre lütfen (dakika): "))
    except ValueError:
        speak("Geçerli bir süre girmediniz. Uyku modu iptal edildi.")
        return

    speak(f"Uyku moduna geçiyorum. {süre} dakika sonra otomatik uyanacağım.")
    bitis_zamani = time.time() + süre * 60
    recognizer = sr.Recognizer()

    while time.time() < bitis_zamani:
        print("Uyku modundayım... (Komut: 'Fatih uyan')")
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                komut = recognizer.recognize_google(audio, language='tr-TR').lower()

                if "fatih uyan" in komut:
                    speak("Uyandım! Fatih emrinize hazır")
                    return
        except sr.UnknownValueError:
            continue  # Anlaşılamayan ses için döngüye devam et
        except Exception as e:
            print(f"Hata oluştu: {e}")
            continue

    speak("Süre doldu. Uyandım!")


def listen_continuously():
    while True:
        command = get_audio_input()

        if "uyku" in command:
            uyku_modu()

        elif "çıkış" in command:
            speak("Asistan kapatılıyor.")
            exit()

        elif "selam" in command or "selamünaleyküm" in command:
            speak("Selam ota60")

        elif "kapat" in command:
            speak("Bilgisayarınızı kapatmamı ister misiniz?")
            if input("İşlem yapılmasını ister misiniz? (Evet/Hayır): ").lower() == "evet":
                os.system("shutdown /s /f /t 0")

        elif "internete gir" in command:
            speak("Chrome tarayıcısı açılıyor.")
            os.system("start chrome.exe")

        elif "yazı yazacağım" in command:
            os.system("start notepad.exe")
            speak("Notepad açılıyor.")

        elif "video izleyeceğim" in command:
            speak("YouTube açılıyor.")
            os.system("start chrome.exe https://www.youtube.com")

        elif "arama yap" in command:
            speak("Ne aramak istersiniz?")
            arama = get_audio_input()
            if arama:
                speak(f"{arama} için Google'da arama yapılıyor.")
                webbrowser.open(f"https://www.google.com/search?q={arama}")
            else:
                speak("Bir şey anlayamadım, lütfen tekrar deneyin.")

        elif "ilahi aç" in command:
            speak("YouTube'dan ilahi açılıyor.")
            os.system("start chrome.exe https://www.youtube.com/watch?v=lLfjr9V3B5E")

        elif "yardım" in command:
            speak("Komutlar listesi okunuyor.")
            help()

        elif "saat kaç" in command:
            speak(datetime.datetime("%H:%M:%S"))


def start_assistant():
    listen_thread = threading.Thread(target=listen_continuously)
    listen_thread.daemon = True
    listen_thread.start()

    while True:
        time.sleep(1)


start_assistant()
