import os
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def find_all_executables(root_dir):
    executables = []
    
    # Add standard system directories
    standard_dirs = [os.path.expandvars('%ProgramFiles%'), os.path.expandvars('%ProgramFiles(x86)%'),
                     os.path.expandvars('%AppData%'), os.path.expandvars('%LocalAppData%')]
    
    for root_dir in standard_dirs:
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.lower().endswith('.exe'):
                    executables.append(os.path.join(root, file))
    
    return executables

# Main function
def open_application(user_input, user_name, user_settings, app_instance, log_message):
    root_dir = os.path.expanduser('~')  # Move root_dir inside the function
    user_input_split = user_input.split("open ")[1]  # Split the input and get the second part
    input_lower = user_input_split.lower()  # Convert to lowercase
    message = f"Searching for {user_input_split}"
    log_message(f"{user_name}: {user_input_split}")

    # Initialize variables to store the best matching executable and its similarity score
    best_match_exe = None
    best_similarity = 0

    app_instance.speak(message)
    # Find all executable files starting from the specified root directory
    all_executables = find_all_executables(root_dir)

    # Iterate through all executable files
    for exe_path in all_executables:
        exe_name = os.path.splitext(os.path.basename(exe_path))[0]
        similarity = similar(input_lower, exe_name.lower())
        if similarity > best_similarity:
            best_similarity = similarity
            best_match_exe = exe_path

    # Check if similarity is above the threshold
    if best_similarity >= 0.7:
        # Open the best matching executable
        message = f"Opening {user_input_split}"
        app_instance.speak(message)
        log_message(f"{user_name}: {user_input_split}")
        app_instance.add_to_message_log(message)
        os.startfile(best_match_exe)
    else:
        message = f"No application found matching {user_input_split}"
        app_instance.speak(message)
        log_message(f"{user_name}: {user_input_split}")
        app_instance.add_to_message_log(message)