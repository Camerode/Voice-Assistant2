from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def command_volume(user_input, user_name, user_settings, app_instance, log_message):
    # Split the user input based on "volume set" or "volume"
    if "volume set " in user_input:
        user_input_split = user_input.split("volume set")
    else:
        user_input_split = user_input.split("volume")
    
    # Extract the volume level from the split
    volume_level = None
    if len(user_input_split) > 1:
        # Check if the volume level is specified after "volume set"
        volume_str = user_input_split[-1].strip()
        # Try converting to a numerical value
        try:
            volume_level = int(volume_str)
        except ValueError:
            # If it's not a numerical value, try converting from textual representation
            textual_numbers = {
                'zero': 0, 'one': 10, 'two': 20, 'three': 30, 'four': 40,
                'five': 50, 'six': 60, 'seven': 70, 'eight': 80, 'nine': 90,
                'ten': 10, 'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50,
                'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90,
                'hundred': 100
            }
            volume_level = textual_numbers.get(volume_str.lower(), None)
    
    if volume_level is not None:
        # Convert to percentage if it's not already
        if volume_level <= 100:
            volume_level /= 100  # Convert to percentage
        set_volume_windows(volume_level * 100)
        message = f"Volume set to {volume_level * 100}%."
        app_instance.speak(message)
        log_message(f"{user_name}: {user_input}")
        app_instance.add_to_message_log(message)
    else:
        # If volume level cannot be determined from the user input
        message = "Volume level not recognized."
        app_instance.speak(message)
        log_message(f"{user_name}: {user_input}")
        app_instance.add_to_message_log(message)

def set_volume_windows(volume2):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # Convert percent to a scalar value between 0 and 1
    scalar = float(volume2) / 100.0
    # Set the volume
    volume.SetMasterVolumeLevelScalar(scalar, None)
