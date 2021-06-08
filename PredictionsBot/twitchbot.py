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
        if not ctx.author.is_mod or not ctx.content.startswith(os.getenv('BOT_PREFIX')):
            return
        print(ctx.author.name + ": " + ctx.content)
        await self.handle_commands(ctx)

    DEBUG = str(os.getenv('DEBUG')).lower()
    if DEBUG != "true":
        # Go away CommandNotFound
        async def event_error(self, error, data=None):
            pass


bot = TwitchBot()


@bot.command(name='ping')
async def ping(ctx):
    'Ping the bot to check if it\'s online'
    await ctx.send("pong!")


@bot.command(name='stats')
async def stats(ctx):
    'Get the stats from the most recent game'
    val.deathmatchCheck(bot)
    if val.deathmatch == False:
        if val.roundsWon > val.roundsLost:
            result = "Yes"
        elif val.roundsWon < val.roundsLost:
            result = "No"
        elif val.roundsWon == val.roundsLost:
            result = "Draw"
        await ctx.send(
            f"Map: {val.mapPlayed} | "
            f"{val.gameTime} | "
            f"rounds played: {val.roundsPlayed} | "
            f"rounds won: {val.roundsWon} | "
            f"rounds lost: {val.roundsLost} | "
            f"K/D/A: {val.KDA} | "
            f"Did they win? {result}"
        )
    else:
        await ctx.send(
            f"{val.gameTime} | "
            f"K/D/A: {val.KDA}"
        )


bot.run()
