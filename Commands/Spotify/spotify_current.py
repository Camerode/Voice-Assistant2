import spotipy

client_id = ""
client_secret = ""
redirect_uri = "" # Noramlly: http://localhost:8888/callback

def spotify_current(user_input, user_name, user_settings, app_instance, log_message):
    sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(client_id,
                                                                client_secret,
                                                                redirect_uri,
                                                                scope="user-read-playback-state"))
    try:
        current_track = sp.current_user_playing_track()
        song = current_track["item"]
        song_artist = current_track["item"]["artists"][0]["name"]
        message = (song['name'] + f" by {song_artist}")
        app_instance.speak(f"Currently playing {message}")
        app_instance.add_to_message_log(f"Currently playing: {message}")
        log_message(f"{user_name} now playing: {message}")
    except Exception as e:
        if "Device not found, reason: None" in str(e):
            error_message = "Device not found, please activate Spotify."
        elif "Restriction violated, reason: UNKNOWN" in str(e):
            error_message = "Reduce command frequency please..."
        else:
            error_message = f"An error occurred: {str(e)}"
        
        app_instance.speak(error_message)
        app_instance.add_to_message_log(error_message)
        log_message(error_message)