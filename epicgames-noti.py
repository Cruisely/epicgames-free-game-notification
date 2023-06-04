import requests
import time
import os
import json
from datetime import datetime, timedelta

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

# Function to check for new free games
def check_for_new_games():
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
                
                release_date = get_release_date(game)  # Get the release date (Thursday)
                
                # Append game and release date to the log file
                append_to_log(game_title, release_date)
                
                app_icon_path = download_app_icon(app_icon_url)
                send_notification_with_icon("New Free Game Out Now!", game_title, app_icon_path, game_url)
                os.remove(app_icon_path)  # Remove the app icon file after use
                
                time.sleep(5)  # Wait for 5 seconds before sending the next notification
        else:
            print("No data found in the response.")
    else:
        print(f"Request failed with status code: {response.status_code}")

# Function to append a game and its release date to the log file
def append_to_log(game_title, release_date):
    if not os.path.exists("game_log.json"):
        log_data = {}
    else:
        with open("game_log.json", "r") as file:
            log_data = json.load(file)

    log_data[game_title] = release_date

    with open("game_log.json", "w") as file:
        json.dump(log_data, file, indent=4)

# Function to get the release date (Thursday) for a game
def get_release_date(game):
    release_date_str = game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['startDate']
    release_date = datetime.strptime(release_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    # Find the Thursday date of the release week
    offset = (3 - release_date.weekday()) % 7  # Calculate the offset to the next Thursday (0 is Monday, 6 is Sunday)
    release_thursday = release_date + timedelta(days=offset)
    
    return release_thursday.strftime("%Y-%m-%d")

# Run the app
while True:
    check_for_new_games()
    time.sleep(60*60)  # Check every hour
