from gtts import gTTS
import requests
import pygame
import time
import playsound

pygame.mixer.init()

# Set to True if you need Debugging Outputs!
debugging: bool = True


def speak(text: str):
    speakObj = gTTS(text=text, lang="de", slow=False)
    speakObj.save("wetter.mp3")
    pygame.mixer.music.load("wetter.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

try:
    url = "https://www.wetter.com/wetter_aktuell/wettervorhersage/3_tagesvorhersage/deutschland/muenchen/DE0006515.html"
    result = requests.get(url, timeout=5)
    forecast = result.text
    teil1 = forecast.split("""<div class="text--white beta palm-inline-block" id="rtw_temp">""")
    teil2 = teil1[1].split("</div>")
    print(teil2[0])
    speak("In München sind es zurzeit " + teil2[0])


except Exception as e:
    if debugging:
        print(e)
    print("Invalid URL or some error occured while making the GET request to the specified URL")
