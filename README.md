# Voice-Assistant2
Meant to be used as a framework/example.
*Made for Windows...*

**Requirements:**
```
pip install SpeechRecognition
pip install pyttsx3
pip install pillow
pip install comtypes
pip install pycaw
pip install spotipy

- Creating a Spotify App: https://developer.spotify.com/dashboard
Make HTTP://localhost:8888/callback the redirect URI, copy secret key and client ID into Spotify files.

- Installing Pybleuz from source: https://github.com/pybluez/pybluez/blob/master/docs/install.rst
Pybleuz can be ignored by removing it from the command mapping, found on line 37 to 39.
```

**Features**
- Spotify control (most playback commands)
- Bluetooth connections
- Create profiles, settings for each of them (custom wake words included), record their usage etc...
- Search and open any .exe files.
- GUI with moving image for when the Assistant speaks, allows text and voice commands
