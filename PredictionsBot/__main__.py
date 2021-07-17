import logging
import os

from discord.ext import commands

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Load the config and tell the user if they need to create one
if os.path.exists("PredictionsBot/config.py"):
    from PredictionsBot.config import Config
    bot = commands.Bot(command_prefix=Config.BOT_PREFIX)
    bot.BOT_PREFIX = Config.BOT_PREFIX
    bot.DEBUG = Config.DEBUG
    try:
        bot.TMI_TOKEN = Config.TMI_TOKEN
        bot.CLIENT_ID = Config.CLIENT_ID
        bot.BOT_NICK = Config.BOT_NICK
        bot.CHANNEL = Config.CHANNEL
        bot.TWITCH_BOT_OWNER = Config.TWITCH_BOT_OWNER
    except:
        pass
    bot.TOKEN = Config.DISCORD_TOKEN
    bot.ROLES = Config.ROLES
    bot.USERNAME = Config.USERNAME
    bot.REGION = Config.REGION
    bot.PUUID = Config.PUUID
else:
    print(
        "config.py not found.\n"
        "Please edit sample_config.py and either rename it or create a new config.py file."
    )
    exit()

if not bot.DEBUG:
    # Don't have a panic attack if someone runs a command the bot doesn't have
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.errors.MissingRole):
            pass

bot.load_extension("PredictionsBot.cogs.discord")
try:
    bot.load_extension("PredictionsBot.cogs.twitch")
except commands.errors.ExtensionFailed:
    pass


bot.run(bot.TOKEN)
