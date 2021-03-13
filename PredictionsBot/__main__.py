from dotenv import load_dotenv
import os


# Load the config and tell the user if they need to create one
if os.path.isfile('config.env'):
    load_dotenv("config.env")
else:
    print(
        "config.env not found.\n"
        "Please edit sample.env and either rename it or create a new config.env file."
    )
    exit()


# Which bot does the user wish to use
if os.getenv('PLATFORM').lower() == 'discord':
    from PredictionsBot import discordbot
elif os.getenv('PLATFORM').lower() == 'twitch':
    from PredictionsBot import twitchbot
