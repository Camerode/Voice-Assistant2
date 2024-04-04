import os
import json
import spotipy

client_id = ""
client_secret = ""
redirect_uri = "" # Noramlly: http://localhost:8888/callback

def spotify_switch_device(user_input, user_name, user_settings, app_instance, log_message):
    try:
        # Extract the desired device from the user input
        device_name = user_input.split("switch to ")[-1].strip().lower()
        
        # Get the profile filename based on the user's name
        profile_filename = f"Profiles/{user_name.lower()}_profile.json"
        
        # Check if the profile file exists
        if os.path.exists(profile_filename):
            # Load the profile from the JSON file
            with open(profile_filename, 'r') as profile_file:
                user_profile = json.load(profile_file)
            
            # Check if the requested device is available in the user settings
            if device_name in user_profile["settings"]["spotify_devices"]:
                # Update the current device in the user settings
                user_profile["settings"]["current_spotify_device"] = device_name
                
                # Save the updated profile back to the JSON file
                with open(profile_filename, 'w') as profile_file:
                    json.dump(user_profile, profile_file, indent=4)
                    
                # Get the device ID from the settings
                device_id = user_profile["settings"]["spotify_devices"][device_name]
                
                # Authenticate with Spotify
                sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(client_id,
                                                                            client_secret,
                                                                            redirect_uri,
                                                                            scope="user-modify-playback-state"))
                # Transfer playback to the new device
                sp.transfer_playback(device_id=device_id, force_play=True)
                
                # Success message
                message = f"Switched Spotify playback device to {device_name}."
                app_instance.speak(message)
                app_instance.add_to_message_log(message)
                log_message(f"{user_name} switched Spotify playback device to {device_name}.")
            else:
                # Device not found in user settings
                message = f"Device '{device_name}' not found in your profile settings."
                app_instance.speak(message)
                app_instance.add_to_message_log(message)
                log_message(f"{user_name} attempted to switch to device '{device_name}', but it was not found.")
        else:
            # Profile file not found
            message = f"Profile file '{profile_filename}' not found."
            app_instance.speak(message)
            app_instance.add_to_message_log(message)
            log_message(f"{user_name} attempted to switch devices, but the profile file was not found.")
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