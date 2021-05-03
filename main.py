from datetime import datetime
import pytesseract as pytes
import numpy as np
import pyttsx3
import speech_recognition as sr
import configparser
import random
import cv2
import os

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
config = configparser.ConfigParser()

listen_command = "glasses"
did_not_understand = "Sorry, I did not understand that, can you repeat?"
online_mode = True
Listening = False
capture = cv2.VideoCapture(0)

pytes.pytesseract.tesseract_cmd = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Pytesseract/tesseract.exe")

with sr.Microphone() as source: sr.Recognizer().adjust_for_ambient_noise(source)

def is_number(string):
    try:
        num=float(string)
        return True
    except ValueError as e:
        return False

def contains_number(string):
    split = string.split(' ')
    for word in split:
        if is_number(word):
            return True
    return False

def listen():

    global Listening

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening")
        audio = r.listen(source)

    speech = ""

    if online_mode:
        try:
            speech = r.recognize_google(audio)
            print("Heard: " + speech)

        except sr.UnknownValueError:
            print("Google Speech Recognition did not understand that")
            if Listening:
                respond(did_not_understand)

        except sr.RequestError as e:
            print("Request Failed; {0}".format(e))
            if Listening:
                respond("There was an unexpected network error")
            Listening = False

    else:
        try:
            speech = r.recognize_sphinx(audio)
            print("Heard: " + speech)

        except sr.UnknownValueError:
            print("Sphinx did not understand that")
            if Listening:
                respond(did_not_understand)

        except sr.RequestError as e:
            print("Request Failed; {0}".format(e))

            if Listening:
                respond("There was an unexpected network error")
            Listening = False

    Listening = False
    return speech

def respond(response):
    print("Responded with: " + response)
    engine.say(response)
    engine.runAndWait()

def assist(message):

    global Listening

    command = message.lower()

    print("Heard command:" + command)

    if listen_command in command:
        Listening = True
        respond("Hey, how can I help?")
        return True

    if "simon says" in command:
        Listening = False
        message = command.replace("simon says", "")
        respond(message)
        return True

    if "what" in command and ("x" in command or "-" in command or "*" in command or "/" in command or "÷" in command or "%" in command or "+" in command or "^" in command):

        Listening = False
        words = command.split(" ")
        calculation = ""

        for word in words:
            if is_number(word) or word=="+" or word=="-" or word=="*" or word=="/" or word=="%" or word=="^" or word=="**" or word=="^" or word=="x":
                calculation+=" "+word

        calculation = calculation.replace("x", "*")
        calculation = calculation.replace("÷", "/")
        calculation = calculation.replace("^", "**")

        calculation_worded = calculation.replace("/", "divided by")
        calculation_worded = calculation_worded.replace("**", "to the power of")
        calculation_worded = calculation_worded.replace("*", "multiplied by")
        calculation_worded = calculation_worded.replace("-", "minus")

        try:
            respond(calculation_worded + " is equal to " + str(eval(calculation)))
        except(EOFError):
            respond("An error has occured when trying to calculate. Try again")

        return True


    if ("thanks" or "thank you") in command:

        Listening = False
        respond("No problem, happy to help")
        return True

    if "number" in command and "between" in command:

        Listening = False
        numbers = []
        for word in command.split(" "):
            if word.replace("-","").isnumeric():
                numbers.append(int(word))
        if(len(numbers) >= 2):
            choosen = random.randint(numbers[0], numbers[1])
            respond("The number I picked is " + str(choosen))

        return True

    if "poggers" in command:
        Listening = False
        respond("Poggers in chat")
        return True

    if "siri" in command or "hey google" in command or "ok google" in command or "alexa" in command:
        Listening = False
        respond("You must be mixing me up with someone else. I am smart glasses")
        return True

    if ("hello" or "hi" or "hey" or "yo" or "good morning") in command:
        Listening = False
        respond("Hello")
        return True

    if "roll" and ("dice" or "die") in command:
        listening = False
        number = random.randint(1,6)
        respond("The number you have rolled is " + str(number))
        return True

    if "flip" and "coin" in command:
        listening = False
        coin = "tails" if random.randint(0,1) == 1 else "heads"
        respond("The coin landed on " + coin)
        return True

    if "what" and "time" in command:
        Listening = False
        respond("It is currently " + datetime.now().strftime("%M past %H"))
        return True

    if "what" and "date" in command:
        Listening = False
        respond("Today is " + datetime.now().strftime("%D"))
        return True


    if "what" and "day" in command:
        Listening = False
        respond("Today is " + datetime.now().strftime("%A"))
        return True

    if "how" and ("doing" or "day" or "are you" in command) in command:
        Listening = False
        respond("I am doing great, thank you")
        return True

    if "what" in command and "can you" in command and "do" in command:
        Listening = False
        respond("I can do many things, like tell you the time, talk to you and help you out. I am your personal assistant")
        return True

    if ("what" or "who" in command) and "are you" in command:
        Listening = False
        respond("I am smart glasses, your personal assistant")
        return True

    if "beatbox" in command:
        Listening = False
        respond("Sure, here goes nothing. boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats and boots and cats")
        return True

    if ("change" in command or "set" in command) and "voice" in command and ("male" in command or "man" in command) and not "female" in command:
        Listening = False
        engine.setProperty('voice', voices[0].id)
        config.set("main", "femalevoice", "False")
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        respond("Set voice to male")
        return True

    if (("change" or "set") and "voice" and ("female" or "woman")) in command:
        Listening = False
        engine.setProperty('voice', voices[1].id)
        config.set("main", "femalevoice", "True")
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        respond("Set voice to female")
        return True

    if ("change" or "set") in command and "voice" in command:

        Listen = False

        respond("What would you like to change the voice to?")
        voice = listen()

        if ("woman" or "female" or "girl") in voice:
            engine.setProperty('voice', voices[1].id)
            config.set("main", "femalevoice", "False")
            respond("Set voice to female")
        elif("man" or "male" or "boy" or "mail") in voice:
            engine.setProperty('voice', voices[0].id)
            config.set("main", "malevoice", "False")
            respond("Set voice to male")

        return True

    if "read" in command:

        Listen = False

        if(capture.isOpened() == False or capture == None):
            respond("Sorry, I couldn't find a camera")
            return False

        image = capture.read()[1]
        image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        gray = cv2.bilateralFilter(gray, 9, 15, 15)
        img_bin = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        gray = cv2.bitwise_not(img_bin)
        kernel = np.ones((2, 1), np.uint8)
        img = cv2.erode(gray, kernel, iterations=1)
        img = cv2.dilate(img, kernel, iterations=1)

        result = pytes.image_to_string(img)

        if(result != '' and result != '' and result!=' '):
            respond(result)
        else:
            respond("Sorry, I cannot read this text")
            return False

        return True

    if "volume" in command and contains_number(command):

        words = command.split(' ')
        volume = ''
        volume_real = ''

        for word in words:
            if is_number(word):
                volume = int(word)/100
                volume_real = int(word)
                break

        if volume != '':
            engine.setProperty("volume", volume)
            respond("Set volume to " + str(volume_real))

        return True

    if "volume" in command:

        volume = engine.getProperty("volume")
        respond("The current volume is set to " + str(int(volume*100)))

        return True

    if ("rate" or "tempo" or "speed") in command and contains_number(command):

        words = command.split(' ')
        tempo = ''

        for word in words:
            if is_number(word):
                tempo = int(word)
                break

        if tempo != '':
            engine.setProperty("rate", tempo)
            respond("Set speech rate to " + str(tempo))

        return True

    if ("tempo" or "speed" or "rate") in command:
        rate = engine.getProperty("rate")
        respond("The current speech rate is set to " + str(rate))
        return True

    return False

if online_mode == False:
    respond("You are currently not connected to the internet, some features will not work and the voice recognition won't be accurate")

config.read('config.ini')
if(config.getboolean("main", "femalevoice")):
    engine.setProperty('voice', voices[1].id)
else:
    engine.setProperty('voice', voices[0].id)

while True:

    if(Listening == False):
        if(listen_command in listen()):
            print("Listening to command")
            Listening = True
            respond("Hi, how can I help?")
            assist(listen())
    else:
        assist(listen())
