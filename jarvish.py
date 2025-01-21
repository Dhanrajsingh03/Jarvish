import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import subprocess
import pyautogui
import yt_dlp

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Function to make the assistant speak"""
    engine.say(text)
    engine.runAndWait()

def greet_user():
    """Function to greet the user based on the time"""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("tora mayi k. How can I assist you today?")

def take_command():
    """Function to take voice input from the user"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {command}")
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return "None"
    except sr.RequestError as e:
        print("Error connecting to Google Speech Recognition API.")
        return "None"
    return command.lower()

def play_music_on_youtube(query):
    """Search and play the song on YouTube"""
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioquality': 1,
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(f"ytsearch:{query}", download=False)
            video_url = result['entries'][0]['url']
            speak(f"Playing {query} on YouTube")
            webbrowser.open(video_url)
        except Exception as e:
            speak(f"Sorry, I couldn't find {query} on YouTube. Error: {str(e)}")

def open_application(app_name):
    """Function to open applications like Notepad, Calculator"""
    try:
        if app_name == "notepad":
            subprocess.run("notepad.exe")
            speak("Opening Notepad")
        elif app_name == "calculator":
            subprocess.run("calc.exe")
            speak("Opening Calculator")
        elif app_name == "chrome":
            subprocess.run("chrome.exe")
            speak("Opening Chrome")
        else:
            speak(f"I cannot open {app_name}")
    except Exception as e:
        speak(f"Sorry, I couldn't open {app_name}. Error: {str(e)}")

def take_screenshot():
    """Function to take a screenshot"""
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    speak("Screenshot taken and saved as screenshot.png")

def shutdown_pc():
    """Function to shutdown the PC"""
    speak("Shutting down the PC")
    subprocess.run(["shutdown", "/s", "/f", "/t", "0"])

def restart_pc():
    """Function to restart the PC"""
    speak("Restarting the PC")
    subprocess.run(["shutdown", "/r", "/f", "/t", "0"])

def control_volume(action):
    """Function to control the system volume (Mute, Unmute, Volume Up, Volume Down)"""
    if action == 'mute':
        subprocess.run("nircmd.exe mutesysvolume 1")
        speak("System volume muted")
    elif action == 'unmute':
        subprocess.run("nircmd.exe mutesysvolume 0")
        speak("System volume unmuted")
    elif action == 'volume up':
        subprocess.run("nircmd.exe changesysvolume 5000")
        speak("Volume increased")
    elif action == 'volume down':
        subprocess.run("nircmd.exe changesysvolume -5000")
        speak("Volume decreased")

def process_random_commands(command):
    """Process random commands by looking for keywords"""
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {current_time}")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open notepad" in command:
        open_application("notepad")

    elif "open calculator" in command:
        open_application("calculator")

    elif "open chrome" in command:
        open_application("chrome")

    elif "play music" in command:
        speak("What song would you like to play?")
        song_name = take_command()
        play_music_on_youtube(song_name)

    elif "take screenshot" in command:
        take_screenshot()

    elif "shutdown" in command:
        shutdown_pc()

    elif "restart" in command:
        restart_pc()

    elif "mute volume" in command:
        control_volume('mute')

    elif "unmute volume" in command:
        control_volume('unmute')

    elif "volume up" in command:
        control_volume('volume up')

    elif "volume down" in command:
        control_volume('volume down')

    elif "exit" in command or "stop" in command:
        speak("Goodbye! Have a great day.")
        return False

    else:
        speak("Sorry, I didn't understand that. Can you try again?")
        print(f"Unrecognized command: {command}")
    
    return True

def main():
    greet_user()
    while True:
        query = take_command()
        
        if query != "None":
            continue_processing = process_random_commands(query)
            if not continue_processing:
                break

if __name__ == "__main__":
    main()