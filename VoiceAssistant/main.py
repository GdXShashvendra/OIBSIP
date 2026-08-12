import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser


# -----------------------------
# Text-to-Speech Setup
# -----------------------------
engine = pyttsx3.init()

engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

# Select voice
voices = engine.getProperty("voices")
if voices:
    engine.setProperty("voice", voices[0].id)


def speak(text):
    """Convert text to speech."""
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


# -----------------------------
# Voice Recognition
# -----------------------------
def take_command():
    """Listen to the user's voice and convert it to text."""

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("\nListening...")

        # Adjust for background noise
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
            return ""

    try:
        print("Recognizing...")

        command = recognizer.recognize_google(audio)

        print("You:", command)

        return command.lower()

    except sr.UnknownValueError:

        speak("Sorry, I didn't understand. Please say that again.")
        return ""

    except sr.RequestError:

        speak("Sorry, the speech recognition service is unavailable.")
        return ""


# -----------------------------
# Greeting
# -----------------------------
def greet():
    current_hour = datetime.datetime.now().hour

    if current_hour < 12:
        greeting = "Good morning!"
    elif current_hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"

    speak(
        f"{greeting} I am your voice assistant. "
        "How can I help you?"
    )


# -----------------------------
# Tell Time
# -----------------------------
def tell_time():

    current_time = datetime.datetime.now().strftime("%I:%M %p")

    speak(f"The current time is {current_time}")


# -----------------------------
# Tell Date
# -----------------------------
def tell_date():

    current_date = datetime.datetime.now().strftime(
        "%d %B %Y"
    )

    speak(f"Today's date is {current_date}")


# -----------------------------
# Google Search
# -----------------------------
def search_web(query):

    query = query.strip()

    if not query:
        speak("What would you like me to search for?")
        return

    speak(f"Searching for {query}")

    search_url = (
        "https://www.google.com/search?q="
        + query.replace(" ", "+")
    )

    webbrowser.open(search_url)


# -----------------------------
# Process Commands
# -----------------------------
def process_command(command):

    if not command:
        return True

    # Hello
    if "hello" in command or "hi" in command:

        speak("Hello! Nice to hear from you.")

    # Time
    elif "time" in command:

        tell_time()

    # Date
    elif "date" in command or "today" in command:

        tell_date()

    # Search
    elif command.startswith("search"):

        query = command.replace("search", "", 1)

        search_web(query)

    # Google
    elif "open google" in command:

        speak("Opening Google.")

        webbrowser.open("https://www.google.com")

    # YouTube
    elif "open youtube" in command:

        speak("Opening YouTube.")

        webbrowser.open("https://www.youtube.com")

    # Goodbye / Exit
    elif (
        "exit" in command
        or "quit" in command
        or "stop" in command
        or "goodbye" in command
    ):

        speak("Goodbye! Have a great day.")

        return False

    # Unknown command
    else:

        speak(
            "Sorry, I don't know that command. "
            "Please try again."
        )

    return True


# -----------------------------
# Main Program
# -----------------------------
def main():

    greet()

    while True:

        command = take_command()

        if not process_command(command):
            break


# Start assistant
if __name__ == "__main__":
    main()