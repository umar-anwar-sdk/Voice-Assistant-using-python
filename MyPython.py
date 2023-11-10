import datetime
import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import os
import requests  # Add this import for making API requests

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your friend sir. Please tell me how may I help you")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-pk')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"
    return query


def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        speak(f'Temperature in {city}: {temperature}°C, Description: {description}')
    else:
        speak(f'Error: Unable to fetch weather data. Status Code: {response.status_code}')


if __name__ == "__main__":
    api_key = '9796ee458eb8efeeeaf5e361db8bb065'  # Replace with your OpenWeatherMap API key
    city = 'Saddiqabad, PK'  # Replace with the name of the city for which you want weather updates
    wishMe()

    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak("searching Wikipedia..")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=1)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open chat bot' in query:
            webbrowser.open("chatgpt.com")

        elif 'play music' in query:
            music_dir = 'C:\\Users\\Omer\\Desktop\\Song'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[1]))

        elif 'time' in query:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir the Time is {strtime}")

        elif 'open code' in query:
            code_path = "C:\\Program Files\\Sublime Text\\sublime_text.exe"
            os.startfile(code_path)

        elif 'weather update' in query:
            get_weather(api_key, city)
