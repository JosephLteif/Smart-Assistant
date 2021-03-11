#imports
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import sys
import os
from weather import weather
import psutil

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')

#setting up the voice rate and the type
engine.setProperty('rate', 130)
engine.setProperty('voice', voices[1].id)

#function that let the engine talk
def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            listener.adjust_for_ambient_noise(source,duration=1)
            voice = listener.listen(source, timeout=3, phrase_time_limit=5)
            command = listener.recognize_google(voice,language="en-US")
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)

    except:
        pass
    return command

def Boot_Assistant():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source,duration=1)
            voice = listener.listen(source, timeout=3, phrase_time_limit=5)
            command = listener.recognize_google(voice,language="en-US")
            command = command.lower()
            print(command)
            if 'hello alexa' in command:
                talk("Hello {}".format(os.getlogin()))
                run_alexa()

    except:
        pass


def run_alexa():

    command = take_command()
    print(command)

    if 'play' in command:
        song = command.replace('play', '')
        talk('playing' + song)
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk('The current time is ' + time)

    elif 'search for' in command:
        search_thing = command.replace('search for', '')
        result_info = wikipedia.summary(search_thing, 2)
        talk('This is a quick summary about ' + search_thing)
        print(result_info)
        talk(result_info)

    elif 'date' in command:
        date = datetime.date.today()
        print(str(date))
        talk("today it's " + str(date))

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        print(joke)
        talk(joke)

    elif 'thank you' in command:
        talk("you're welcome " + os.getlogin())
        sys.exit()

    elif 'ocr' in command:
        talk("Sure thing!")
        import OCR

    elif 'face detection' in command:
        talk("Sure thing!")
        import FaceDetection
    
    elif 'weather of' in command:
        location = command.replace('weather of','')
        info_dict = weather(location)
        talk("it's " + info_dict["weather description"] + "today with a temperature of " + str(info_dict["temperature"]))

    elif 'statistics' in command:
        battery = psutil.sensors_battery()
        print("Current Battery percentage is {}%".format(battery.percent))
        print("the cpu is at {}%".format(psutil.cpu_percent()))
        print('RAM memory is at {} %'.format(psutil.virtual_memory()[2]))
        talk("Current Battery percentage is {}%".format(battery.percent)) 
        if battery.power_plugged:
            talk("And is currently charging.")
        talk("the cpu is at {}%".format(psutil.cpu_percent()))
        talk('RAM memory is at {} %'.format(psutil.virtual_memory()[2]))
        
    else:
        talk("Could you please repeat ? I didn't understand")
    
    run_alexa()


while True:
    Boot_Assistant()
