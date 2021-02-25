import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import sys
import os

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')

engine.setProperty('rate', 130)
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:

        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)

    except:
        pass
    return command


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
        from OCR import funct
        funct()

    elif 'face detection' in command:
        talk("Sure thing!")
        from FaceDetection import funct
        funct()

    else:
        talk("Could you please repeat ? I didn't understand")


while True:
    run_alexa()
