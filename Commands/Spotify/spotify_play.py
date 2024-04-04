import spotipy
import spotipy.oauth2
from fuzzywuzzy import process

client_id = ""
client_secret = ""
redirect_uri = "" # Noramlly: http://localhost:8888/callback

def spotify_play(user_input, user_name, user_settings, app_instance, log_message):
    try:
        if "play" in user_input:
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
                song_artist_input = user_input.split("play", 1)[1].strip()
                
                # Split the input into song and artist using fuzzy matching
                choices = [track["name"] + " " + ", ".join([artist["name"] for artist in track["artists"]]) for track in sp.search(song_artist_input, limit=10, type='track')['tracks']['items']]
                song_artist, score = process.extractOne(song_artist_input, choices)
                
                res = sp.search(song_artist, type='track,artist')

                # Extract the first track's ID
                first_track_id = res['tracks']['items'][0]['id']

                # Extract the artist name and track name of the first track
                artist_name = res['tracks']['items'][0]['artists'][0]['name']
                track_name = res['tracks']['items'][0]['name']

                track_uri = f"spotify:track:{first_track_id}"
                sp.add_to_queue(track_uri, device_token)
                message = f"Added {track_name} by {artist_name} to queue."
                app_instance.speak(message)
                app_instance.add_to_message_log(message)
                log_message(f"{user_name} added {track_name} by {artist_name} to queue...")

            else:
                # Current Spotify device token not found in user settings
                message = "Current Spotify playback device token not found in your profile settings."
                app_instance.speak(message)
                app_instance.add_to_message_log(message)
                log_message(f"{user_name} attempted to skip playback, but current Spotify device token was not found.")
        else:
            message = "Invalid command for skipping playback."
            app_instance.speak(message)
            app_instance.add_to_message_log(message)
            log_message(f"{user_name} attempted an invalid command for skipping playback.")
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
