import os

from discord.ext import commands
from dotenv import load_dotenv

# Load the config and tell the user if they need to create one
if os.path.isfile('config.env'):
    load_dotenv("config.env")
else:
    print(
        "config.env not found.\n"
        "Please edit sample.env and either rename it or create a new config.env file."
    )
    exit()

TOKEN = str(os.getenv('DISCORD_TOKEN'))
DEBUG = str(os.getenv('DEBUG')).lower()
bot = commands.Bot(command_prefix=os.getenv('BOT_PREFIX'))

if DEBUG != "true":
    # Don't have a panic attack if someone runs a command the bot doesn't have
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.errors.MissingRole):
            pass

bot.load_extension("PredictionsBot.cogs.discord")
# I'd put these in the same try catch but since I'm lazy and use this bot also as my own twitch bot in a `personal` cog it's just easier this way.
try:
    bot.load_extension("PredictionsBot.cogs.twitch")
except commands.errors.ExtensionFailed:
    pass
try:
    if os.path.isfile('PredictionsBot/cogs/personal.py'):
        bot.load_extension("PredictionsBot.cogs.personal")
except commands.errors.ExtensionFailed:
    pass


bot.run(TOKEN)
