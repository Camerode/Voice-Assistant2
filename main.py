import tkinter as tk
import threading
import speech_recognition as sr
import pyttsx3
from datetime import datetime
from PIL import Image, ImageTk, ImageSequence
import json
import os
from difflib import SequenceMatcher
import logging
import random
from Commands import commandEXAMPLE, open_application, volume
from Commands.Bluetooth import bluetooth_discover, bluetooth_pair
from Commands.Spotify import spotify_resume, spotify_switch_device, spotify_pause, spotify_skip, spotify_current, spotify_back, spotify_play, spotify_devices
from Commands.Search import search_temu, search_amazon, search_anime, search_tv, search_youtube
# Commands mapping
# "Input for command to activate": file_name.function_name
COMMAND_FUNCTIONS = {
    "commandEXAMPLE": commandEXAMPLE.commandEXAMPLE,
    # Spotify
    "devices": spotify_devices.spotify_devices,
    "back": spotify_back.spotify_back,
    "current": spotify_current.spotify_current,
    "pause": spotify_pause.spotify_pause,
    "play": spotify_play.spotify_play,
    "resume": spotify_resume.spotify_resume,
    "skip": spotify_skip.spotify_skip,
    "switch to": spotify_switch_device.spotify_switch_device,
    # Search
    "search temu": search_temu.search_temu,
    "search amazon": search_amazon.search_amazon,
    "search anime": search_anime.search_anime,
    "search tv": search_tv.search_tv,
    "search shows": search_tv.search_tv,
    "search movies": search_tv.search_tv,
    "search youtube": search_youtube.search_youtube,
    # Bluetooth
    "discover": bluetooth_discover.bluetooth_discover,
    "connect to": bluetooth_pair.bluetooth_pair,
    # Open
    "open": open_application.open_application,
    # Volume
    "volume": volume.command_volume
}

def log_message(message):
    logging.getLogger("comtypes").setLevel(logging.ERROR)
    logging.basicConfig(filename='records.log', format='%(message)s', level=logging.INFO)
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d/%m/%Y %H:%M:%S")
    logging.info(f"{formatted_datetime}: {message}")
def log_session_end():
    logging.getLogger("comtypes").setLevel(logging.ERROR)
    logging.basicConfig(filename='records.log', format='%(message)s', level=logging.INFO)
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d/%m/%Y %H:%M:%S")
    logging.info(f"{formatted_datetime}: Session ended.")
def log_session_quit():
    logging.getLogger("comtypes").setLevel(logging.ERROR)
    logging.basicConfig(filename='records.log', format='%(message)s', level=logging.INFO)
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d/%m/%Y %H:%M:%S")
    logging.info(f"{formatted_datetime}: Window closed.")
    root.destroy()

class UserProfile:
    def __init__(self, name, settings):
        self.name = name
        self.settings = settings

class App:
    def __init__(self, root):
        self.root = root
        self.current_user = None  # Initialize current user as None
        # Load user profiles from JSON
        self.user_profiles = self.load_user_profiles()
        # Setting title
        root.title("Virtual Assistant")
        # Setting window size
        width = 530
        height = 300    
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        # Initialize speech recognition
        self.recognizer = sr.Recognizer()

        # Initialize gif_index
        self.gif_index = 0
        # Preload and resize talk.gif in a separate thread
        self.gif_thread = threading.Thread(target=self.load_and_resize_gif, args=("talk.gif",))
        self.gif_thread.daemon = True
        self.gif_thread.start()

        # Create GUI elements
        self.create_widgets()

        # Start the voice recognition thread
        self.voice_thread = threading.Thread(target=self.listen_voice)
        self.voice_thread.daemon = True
        self.voice_thread.start()

        # Flag to indicate whether the assistant is speaking
        self.is_speaking_event = threading.Event()
        # Flag to indicate whether the assistant is activated
        self.is_activated = False

        # Load intents from JSON
        self.intents = self.load_intents("intents.json")

    def create_widgets(self):
        self.user_input = tk.StringVar()
        # User input entry
        self.entry_user_input = tk.Entry(self.root, textvariable=self.user_input)
        self.entry_user_input.place(x=10, y=270, width=200, height=20)
        self.entry_user_input.bind('<Return>', self.send_command)
        # Send button
        self.btn_send = tk.Button(self.root, text="Send", command=self.send_command)
        self.btn_send.place(x=210, y=270, width=40, height=20)
        # Assistant output text widget
        self.lbl_assistant_output = tk.Text(self.root, bg="#3e3e3e", fg="#ffffff", wrap="word")
        self.lbl_assistant_output.place(x=270, y=9, width=240, height=281)
        # Scrollbar for the message log
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.lbl_assistant_output.yview)
        self.scrollbar.place(x=510, y=9, height=281)
        # Attach scrollbar to the text widget
        self.lbl_assistant_output.config(yscrollcommand=self.scrollbar.set)
        # Set initial image
        self.image_label = tk.Label(self.root, bg="#3e3e3e")
        self.image_label.place(x=10, y=10, width=240, height=240)
        # Initialize message log
        self.message_log = ""

    def load_intents(self, filename):
        with open(filename, 'r') as file:
            intents = json.load(file)
        return intents['intents']
    
    def load_user_profiles(self):
        user_profiles = {}
        # Load user profiles from Profiles folder
        profile_files = os.listdir("Profiles")
        for filename in profile_files:
            if filename.endswith(".json"):
                with open(os.path.join("Profiles", filename), 'r') as file:
                    profile_data = json.load(file)
                    user_profile = UserProfile(profile_data['name'], profile_data['settings'])
                    user_profiles[profile_data['name']] = user_profile
        return user_profiles

    def listen_voice(self):
        while True:
            with sr.Microphone() as source:
                try:
                    audio_data = self.recognizer.listen(source)
                    user_input = self.recognizer.recognize_google(audio_data).lower()
                    if not self.is_activated:
                        for user_name, user_profile in self.user_profiles.items():
                            wake_word = user_profile.settings.get("wake_word", "").lower()
                            if wake_word and wake_word in user_input:
                                self.is_activated = True
                                self.current_user = user_profile
                                hour = datetime.now().hour
                                log_message("Assistant activated.")
                                if hour >= 0 and hour < 12:
                                    self.speak(f"Good Morning {user_name}!")
                                elif hour >= 12 and hour < 16:
                                    self.speak(f"Good Afternoon {user_name}!")
                                else: 
                                    self.speak(f"Good Evening {user_name}!")
                                break
                    else:
                        self.process_input(user_input)
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
                except sr.UnknownValueError:
                    pass
                except Exception as e:
                    print("An error occurred: {0}".format(e))

    def send_command(self, event=None):
        user_input = self.user_input.get().strip().lower()
        self.user_input.set("")
        if self.is_activated:
            if user_input == "sleep":
                self.is_activated = False
                log_session_end()
                self.speak("Deactivating...")
            else:
                self.process_input(user_input)
        else:
            for user_name, user_profile in self.user_profiles.items():
                wake_word = user_profile.settings.get("wake_word", "").lower()
                if wake_word and wake_word in user_input.lower():
                    self.is_activated = True
                    self.current_user = user_profile
                    hour = datetime.now().hour
                    log_message("Assistant activated.")
                    if hour >= 0 and hour < 12:
                        self.speak(f"Good Morning {user_name}!")
                    elif hour >= 12 and hour < 16:
                        self.speak(f"Good Afternoon {user_name}!")
                    else:
                        self.speak(f"Good Evening {user_name}!")    
                    break

    def process_input(self, user_input):
        # Get user profile details
        user_name = self.current_user.name
        user_settings = self.current_user.settings
        log_message(f"{user_name}: {user_input}")

        # Check if the user input matches any command
        for command, command_function in COMMAND_FUNCTIONS.items():
            if user_input.startswith(command):
                command_function(user_input, user_name, user_settings, self, log_message)
                return

        # If no command is matched, check for intent match
        matched_intent = self.match_intent(user_input)
        self.add_to_message_log(f"{self.current_user.name}: {user_input}")

        if matched_intent:
            responses = matched_intent['responses']
            response = random.choice(responses)  # Randomly select a response
            response_with_name = response.replace("{user_name}", self.current_user.name)
            self.add_to_message_log("Bot: " + response_with_name)
            log_message(f"Bot: {response_with_name}")
            self.speak(response_with_name)
        else:
            # If no intent is matched, provide a default response
            default_response = "Could you be more specific please!"
            self.add_to_message_log("Bot: " + default_response)
            log_message("Bot: " + default_response)
            self.speak(default_response)

    def match_intent(self, user_input):
        best_match = None
        best_ratio = 0.0
        for intent in self.intents:
            for pattern in intent['pattern']:
                ratio = SequenceMatcher(None, user_input, pattern).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_match = intent
        if best_ratio >= 0.6:  # Minimum similarity threshold (60% default)
            return best_match
        else:
            return None

    def add_to_message_log(self, message):
        self.lbl_assistant_output.insert(tk.END, message + "\n")
        self.lbl_assistant_output.see(tk.END)

    def speak(self, text):
        self.gif_index = 0  # Reset gif_index
        self.is_speaking_event.set()  # Start animation
        # Speak text in a separate thread
        threading.Thread(target=self.speak_thread, args=(text,)).start()

    def speak_thread(self, text):
        try:
            # Speak text
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            # Stop animation
            self.is_speaking_event.clear()
        except RuntimeError as e:
            if 'run loop already started' in str(e):
                pass
            else:
                print(f"Error in speak_thread: {e}")

    def load_and_resize_gif(self, filename):
        img = Image.open(filename)
        # Resize each frame of the GIF to fit the label dimensions
        self.talk_gif = [ImageTk.PhotoImage(frame.copy().resize((240, 240))) for frame in ImageSequence.Iterator(img)]
        self.update_animation()

    def update_animation(self):
        if hasattr(self, 'talk_gif') and self.is_speaking_event.is_set():
            # Update image with next frame of talk.gif
            self.image_label.config(image=self.talk_gif[self.gif_index])
            self.gif_index = (self.gif_index + 1) % len(self.talk_gif)
        elif hasattr(self, 'talk_gif'):
            # Freeze image on the current frame
            self.image_label.config(image=self.talk_gif[self.gif_index])
        # Schedule the next update of the animation after 100 milliseconds
        self.root.after(100, self.update_animation)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", log_session_quit)
    root.mainloop()