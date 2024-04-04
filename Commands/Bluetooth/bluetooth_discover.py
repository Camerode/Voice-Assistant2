import bluetooth

def bluetooth_discover(user_input, user_name, user_settings, app_instance, log_message):
    # discover nearby devices
    nearby_devices = bluetooth.discover_devices()
    message_voice = (f"There are {len(nearby_devices)} devices available...")
    app_instance.speak(message_voice)
    log_message(f"{user_name}: {user_input}")
    # print the name and MAC address of each device
    for addr in nearby_devices:
        message = (f"Bluetooth device name: \n{bluetooth.lookup_name(addr), {addr}}\n")
        app_instance.add_to_message_log(message)