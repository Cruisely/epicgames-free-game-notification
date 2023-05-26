import requests
import datetime
import time
import os
import webbrowser

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
                    
                    app_icon_path = download_app_icon(app_icon_url)
                    send_notification_with_icon("New Free Game Out Now!", game_title, app_icon_path, game_url)
                    os.remove(app_icon_path)  # Remove the app icon file after use
                    
                    time.sleep(5)  # Wait for 5 seconds before sending the next notification

# Run the app
while True:
    check_for_new_games()
    time.sleep(60*60)  # Check every hour
