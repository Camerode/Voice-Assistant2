import os
import json
from bluetooth import discover_devices, BluetoothSocket, RFCOMM
import time
import threading

def bluetooth_pair(user_input, user_name, user_settings, app_instance, log_message):
    log_message(f"{user_name}: {user_input}")
    # Create a thread to handle Bluetooth pairing
    bluetooth_thread = threading.Thread(target=bluetooth_pair_thread, args=(user_input, user_name, user_settings, app_instance, log_message))
    # Start the thread
    bluetooth_thread.start()

def bluetooth_pair_thread(user_input, user_name, user_settings, app_instance, log_message):
    try:
        # Construct the path to the profile file
        profile_filename = f"Profiles/{user_name.lower()}_profile.json"
        # Load user profile from JSON file
        with open(profile_filename, 'r') as f:
            user_profile = json.load(f)
        # Extract Bluetooth devices from user profile
        bluetooth_devices = user_profile["settings"]["bluetooth_devices"]
                
        # Splitter
        user_input_split = user_input.split("connect to")
        # Parse user input to extract device name
        user_input_lower = user_input_split[-1].strip().lower()
        for device_name, device_address in bluetooth_devices.items():
            if device_name.lower() == user_input_lower:
                message2 = f"Attempting to connect to {device_name}..."
                app_instance.add_to_message_log(message2)
                app_instance.speak(message2)
                nearby_devices = discover_devices()
                if device_address in nearby_devices:
                    # Perform pairing steps here (e.g., using pybluez)
                    try:
                        # Create a socket connection (RFCOMM in this example)
                        sock = BluetoothSocket(RFCOMM)
                        sock.connect((device_address, 1))
                        # Keep-alive loop: send a keep-alive packet every 10 seconds
                        while True:
                            # Send a keep-alive packet (e.g., a heartbeat)
                            sock.send(b'keep_alive')
                            # Wait for a short interval before sending the next keep-alive packet
                            time.sleep(10)
                    except Exception as e:
                        message3 = f"Failed to connect to {device_name}..."
                        app_instance.add_to_message_log(message3)
                        app_instance.speak(message3)
                else:
                    message4 = f"Device not found nearby: {device_name} ({device_address})"
                    app_instance.add_to_message_log(message4)
                    app_instance.speak(message4)
                break
        else:
            message5 = ("Device mentioned not found in Bluetooth devices.")
            app_instance.add_to_message_log(message5)
            app_instance.speak(message5)
    except FileNotFoundError:
        print(f"Profile file {profile_filename} not found.")
    except json.JSONDecodeError:
        print(f"Error parsing JSON in profile file {profile_filename}.")
