import spotipy

client_id = ""
client_secret = ""
redirect_uri = "" # Noramlly: http://localhost:8888/callback

def spotify_devices(user_input, user_name, user_settings, app_instance, log_message):
    scope = "user-read-playback-state"
    sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(client_id,
                                                                client_secret,
                                                                redirect_uri,
                                                                scope=scope))
    data = sp.devices()
    if data != None:
        devices = data['devices']
        messageVoice = f"There are {len(devices)} devices accessing to your Spotify..."
        app_instance.speak(messageVoice)
        log_message(messageVoice)
        i = 1
        for dev in devices:
            message = (f"{i}: {dev['name']} with id: {dev['id']}")
            app_instance.add_to_message_log(message)
            i+= 1