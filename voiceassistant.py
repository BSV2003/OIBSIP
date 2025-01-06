import speech_recognition as sr
import pyttsx3
import datetime
import time
import threading
import schedule
import webbrowser

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def get_voice_command():
    """Capture voice command using microphone."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            speak("Network error. Please check your connection.")
            return ""
        except Exception as e:
            print(f"Error: {e}")
            return ""

# Reminder storage
reminders = []

def add_reminder(reminder_time, message):
    """Schedule a reminder."""
    def reminder_task():
        speak(f"Reminder: {message}")
        print(f"Reminder: {message}")
    
    schedule.every().day.at(reminder_time).do(reminder_task)
    reminders.append({"time": reminder_time, "message": message})
    speak(f"Reminder set for {reminder_time}.")

def respond_to_command(command):
    """Respond to user commands."""
    if "hello" in command:
        speak("Hello! How can I assist you?")
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}.")
    elif "search" in command:
        speak("What do you want to search for?")
        query = get_voice_command()
        if query:
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
            speak(f"Here are the results for {query}.")
    elif "set reminder" in command:
        speak("What time should I set the reminder? Please say the time in 24-hour format, like 15:30.")
        reminder_time = get_voice_command()
        if reminder_time:
            speak("What should I remind you about?")
            message = get_voice_command()
            if message:
                add_reminder(reminder_time, message)
    elif "list reminders" in command:
        if reminders:
            speak("Here are your reminders:")
            for reminder in reminders:
                speak(f"At {reminder['time']}, {reminder['message']}.")
        else:
            speak("You have no reminders set.")
    else:
        speak("Sorry, I can't perform that task yet.")

def run_scheduler():
    """Continuously run the scheduler in the background."""
    while True:
        schedule.run_pending()
        time.sleep(1)

# Main function
if __name__ == "__main__":
    # Start the scheduler in a background thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    speak("Voice Assistant initialized. How can I help you?")
    while True:
        command = get_voice_command()
        if "exit" in command or "quit" in command:
            speak("Goodbye!")
            break
        elif command:
            respond_to_command(command)
