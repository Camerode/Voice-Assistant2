import webbrowser

def search_tv(user_input, user_name, user_settings, app_instance, log_message):
    try:
        if "tv" in user_input:
            if "for" in user_input:
                split_search = user_input.split("search tv for")[-1]
            else:
                split_search = user_input.split("search tv ")[-1]
        elif "movies" in user_input:
            if "for" in user_input:
                split_search = user_input.split("search movies for")[-1]
            else:
                split_search = user_input.split("search movies ")[-1]
        elif "shows" in user_input:
            if "shows" in user_input:
                split_search = user_input.split("search anime for")[-1]
            else:
                split_search = user_input.split("search anime ")[-1]
        else:
            pass

        message = f"Searching for {split_search}..."
        app_instance.speak(message)
        log_message(f"{user_name}: {user_input}")
        app_instance.add_to_message_log(message)

        url = f"https://soap2day.qa/search/{split_search}"
        webbrowser.open_new_tab(url)

    except Exception as e:
        error_message = str(e)
        app_instance.speak(error_message)
        app_instance.add_to_message_log(error_message)
        log_message(error_message)