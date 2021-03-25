# imports
from chatbot.chatbot import chat
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

# setting up the voice rate and the type
engine.setProperty('rate', 130)
engine.setProperty('voice', voices[1].id)

# function that let the engine talk
def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            listener.adjust_for_ambient_noise(source, duration=1)
            voice = listener.listen(source, timeout=3, phrase_time_limit=5)
            command = listener.recognize_google(voice, language="en-US")
            command = command.lower()
            if 'misty' in command:
                command = command.replace('misty', '')
    except:
        pass
    print(command)
    return command


def Boot_Assistant():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration=1)
            voice = listener.listen(source, timeout=3, phrase_time_limit=5)
            command = listener.recognize_google(voice, language="en-US")
            command = command.lower()
            print(command)
            if 'misty' in command or 'mystic' in command:
                talk("Yes {}".format(os.getlogin()))
                run_misty()

    except:
        pass

def run_misty():

    command = take_command()
    command = chat(command)
    context = command[1]

    if 'greeting' in context:
        talk(command[0])
    
    elif 'options' in context:
        talk(command[0])
        
    elif 'play' in context:
        talk(command[0])
        input = take_command()
        talk('playing' + input)
        pywhatkit.playonyt(input)

    elif 'time' in context:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        response = str(command[0] + time)
        talk(response)

    elif 'search' in context:
        talk(command[0])
        input = take_command()
        search_thing = input.replace('search for', '')
        result_info = wikipedia.summary(search_thing, 2)
        talk('This is a quick summary about ' + search_thing)
        print(result_info)
        talk(result_info)

    elif 'date' in context:
        date = datetime.date.today()
        response = str(command[0] + date)
        print(response)
        talk(response)

    elif 'joke' in context:
        talk(command[0])
        joke = pyjokes.get_joke()
        print(joke)
        talk(joke)

    elif 'thanks' in context or 'goodbye' in context:
        response = str(command[0] + os.getlogin())
        talk(response)
        sys.exit()

    elif 'optical character recognition' in context:
        talk(command[0])
        import OCR

    elif 'face detection' in context:
        talk(command[0])
        import FaceDetection

    elif 'weather' in context:
        talk(command[0])
        input = take_command()
        location = input.replace('weather of', '')
        info_dict = weather(location)
        talk("it's " + info_dict["weather description"] +
             "today with a temperature of " + str(info_dict["temperature"]))

    elif 'statistics' in context:
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

    run_misty()


while True:
    Boot_Assistant()
