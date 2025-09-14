import speech_recognition as sr

r = sr.Recognizer()
with sr.AudioFile("audio.wav") as source:
    audio = r.record(source)

text = r.recognize_google(audio, language="es-ES")
print(text)