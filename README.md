# Epic Games Free Game Notification
**NOTE** This script is currently only for MacOS 
---
This Python script is an automatic notification for the free game that comes out each Thursday on Epic Games

Features of the code include:
- A corresponding image in the notification to the game
- When you click on the notification you will be brought to the store page of the game
- A game log of each game that you've gotten a notification for and the first available date

Hidden code features include:
- A game log will be made if there is not one already
- The game will not be repeated in the log if it is already present 
- It will not send a notification for the "Mystery Game"
---
**MacOS Dependencies**
- requests
> You can install this using
> ```
> pip install requests
> ```
- terminal-notifier
> you can install this using
> ```
> brew install terminal-notifier
> ```

>This **requires** Homebrew which you can install if you haven't already by using 
>
>```
>/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
>```
>
>or for more documentation go [here](https://brew.sh/)
