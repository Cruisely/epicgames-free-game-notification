import requests
import datetime
import time
import os
import webbrowser

LOG_FILE = "game_log.txt"

# Function to send a notification with dynamic app icon
def send_notification_with_icon(title, message, app_icon_path, game_url):
    command = f'terminal-notifier -title "{title}" -message "{message}" -contentImage "{app_icon_path}" -open "{game_url}"'
    os.system(command)

# Function to download the app icon for a game
def download_app_icon(app_icon_url):
    response = requests.get(app_icon_url)
    app_icon_path = 'app_icon.png'
    with open(app_icon_path, 'wb') as f:
        f.write(response.content)
    return app_icon_path

# Function to check if a game is already in the log file
def is_game_in_log(game_title):
    if not os.path.exists(LOG_FILE):
        return False
    with open(LOG_FILE, 'r') as f:
        for line in f:
            if game_title in line:
                return True
    return False

# Function to add a new game to the log file
def add_game_to_log(game_title, first_available_day):
    with open(LOG_FILE, 'a') as f:
        f.write(f"{game_title},{first_available_day}\n")

# Function to check for new free games
def check_for_new_games():
    current_day = datetime.datetime.today().weekday()
    if current_day == 3:  # Thursday (0 is Monday, 6 is Sunday)
        response = requests.get('https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=US&allowCountries=US')
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                for game in data['data']['Catalog']['searchStore']['elements']:
                    game_title = game['title']
                    if game_title == "Mystery Game":
                        continue
                    app_icon_url = game['keyImages'][0]['url']
                    game_url = f"https://www.epicgames.com/store/en-US/product/{game['productSlug']}"
                    first_available_day = datetime.date.today().strftime("%Y-%m-%d")
                    
                    if not is_game_in_log(game_title):
                        app_icon_path = download_app_icon(app_icon_url)
                        send_notification_with_icon("New Free Game Out Now!", game_title, app_icon_path, game_url)
                        add_game_to_log(game_title, first_available_day)
                        os.remove(app_icon_path)  # Remove the app icon file after use
                    
                    time.sleep(5)  # Wait for 5 seconds before sending the next notification

# Create the log file if it's missing
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as f:
        pass

# Run the app
while True:
    check_for_new_games()
    time.sleep(60*60)  # Check every hour
