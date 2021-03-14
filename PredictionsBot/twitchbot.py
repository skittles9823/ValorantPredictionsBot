import os
from twitchio.ext import commands
import PredictionsBot.valorant as val
from dotenv import load_dotenv

load_dotenv("config.env")

class TwitchBot(commands.Bot):
    def __init__(self):
        # Sensitive information loaded from config
        super().__init__(token=os.getenv('TMI_TOKEN'),
                        client_secret=os.getenv('CLIENT_ID'),
                        nick=os.getenv('BOT_NICK'),
                        prefix=os.getenv('BOT_PREFIX'),
                        initial_channels=[os.getenv('CHANNEL')])

    # Record incoming moderator commands to console for logging
    async def event_message(self, ctx):
        if not ctx.author.is_mod or not ctx.content.startswith("!"):
            return
        print(ctx.author.name + ": " + ctx.content)
        await self.handle_commands(ctx)

    # Go away CommandNotFound
    async def event_error(self, error, data=None):
        pass

    # Go away CommandNotFound
    async def event_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            print(f"The command {ctx.message} doesn't seem to exist.")

bot = TwitchBot()


@bot.command(name='ping')
async def ping(ctx):
    'Ping the bot to check if it\'s online'
    await ctx.send("pong!")


@bot.command(name='stats')
async def stats(ctx):
    'Get the stats from the most recent game'
    await ctx.send("Please wait up to 10 seconds for me to retrieve the match info.")
    teamPlayers, roundsPlayed, playerHasWon, roundsWon, roundsLost, KDA = val.getLatestMatchInfo()
    result = "no"
    if playerHasWon != "False":
        result = "yes"
    await ctx.send(
        f"{roundsPlayed} rounds played | "
        f"{roundsWon} rounds won | "
        f"{roundsLost} rounds lost | "
        f"Their KDA was {KDA} | "
        f"Did they win? {result}"
    )


bot.run()