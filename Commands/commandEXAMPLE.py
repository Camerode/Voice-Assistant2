def commandEXAMPLE(user_input, user_name, user_settings, app_instance, log_message):
    # command1 example
    if "commandEXAMPLE" in user_input:
        device_id = user_settings.get("spotify_device")  
        message = f"Hello {user_name}! You said {user_input}, {device_id}"
        app_instance.speak(message)
        log_message(f"{user_name}: {user_input}")
        app_instance.add_to_message_log(message)