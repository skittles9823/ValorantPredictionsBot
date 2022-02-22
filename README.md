# ValorantPredictionsBot

A simple Twitch/Discord bot which can grab the stats most commonly used for Twitch predictions on Valorant games.

# Credits

[Henrik-3](https://github.com/Henrik-3) for his [unofficial valorant api](https://github.com/Henrik-3/unofficial-valorant-api)

# Future plans

In the future, the hope is this bot will be able to end a prediction and also give the correct result so the viewers can have a seamless experience and not get scammed by Pepega mods, this will be worked on as soon as [TwitchIO](https://github.com/TwitchIO/TwitchIO) adds support for the predictions API.

# Usage

1. Install the requirements with pip

```
pip install --user -r requirements.txt
```

2. Create a basic bot instance for Twitch and Discord, you can use Google for this.
3. Rename and edit [sample_config.py](./PredictionsBot/sample_config.py) to config.py with the bots credentials.
4. Find the players Username, Region and PUUID you wish to use and input them in the correct variables.
    - if you wish to use the bot with multiple Valorant accounts, edit [sample_accounts.json](./sample_accounts.json) and rename it to accounts.json, then use the stats command followed by the username to get the stats or switch the bot to use said player.
5. Finally once the config is setup and finished, run the bot with:

```
python3 -m PredictionsBot
```

# Examples

## Twitch

![Twitch](images/Twitch.png)

## Discord

![Discord](images/Discord.png)
