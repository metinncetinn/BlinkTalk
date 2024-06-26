import speech_recognition as sr

def sestt():
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        rec.adjust_for_ambient_noise(source, duration=1)  # Mikrofona ortama uyum sağlaması için zaman tanıyın
        print("I'm listening")
        try:
            audio = rec.listen(source, timeout=5, phrase_time_limit=5)  # Bekleme sürelerini artırın
            text = rec.recognize_google(audio)
            print('You said: ' + text)
            return text
        except sr.UnknownValueError:
            print('I could not understand what you said. Please repeat again.')
        except sr.WaitTimeoutError:
            print("I'm waiting for you to talk. Please start speaking within the time limit.")
        except sr.RequestError:
            print('There was an issue with the request, possibly due to no internet connection.')