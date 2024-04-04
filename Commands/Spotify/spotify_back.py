import spotipy
import spotipy.oauth2

client_id = ""
client_secret = ""
redirect_uri = "" # Noramlly: http://localhost:8888/callback

def spotify_back(user_input, user_name, user_settings, app_instance, log_message):
    try:
        if "back" in user_input:
            # Get the current Spotify device name from the user settings
            device_name = user_settings.get("current_spotify_device")
            # Get the corresponding device token from the spotify_devices dictionary
            device_token = user_settings["spotify_devices"].get(device_name)
            if device_token:
                # Start playback on the current device
                sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(client_id,
                                                                            client_secret,
                                                                            redirect_uri,
                                                                            scope="user-modify-playback-state"))
                sp.next_track(device_token)
                message = "Playing previous song"
                app_instance.add_to_message_log(message)
                app_instance.speak(message)
            else:
                # Current Spotify device token not found in user settings
                message = "Current Spotify playback device token not found in your profile settings."
                app_instance.speak(message)
                app_instance.add_to_message_log(message)
                log_message(f"{user_name} attempted to go back in playback, but current Spotify device token was not found.")
        else:
            message = "Invalid command for going back in playback."
            app_instance.speak(message)
            app_instance.add_to_message_log(message)
            log_message(f"{user_name} attempted an invalid command for going back in playback.")
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