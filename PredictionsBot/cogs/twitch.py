import os
from discord.ext import commands as discord_commands
from twitchio.ext import commands as commands
import PredictionsBot.valorant as val
from dotenv import load_dotenv

load_dotenv("config.env")

class Twitch(discord_commands.Cog):
    def __init__(self, bot):
        self.discord_bot = bot
        self.bot = commands.Bot(
            # set up the bot
            irc_token=os.getenv('TMI_TOKEN'),
            client_secret=os.getenv('CLIENT_ID'),
            nick=os.getenv('BOT_NICK'),
            prefix=os.getenv('BOT_PREFIX'),
            initial_channels=[os.getenv('CHANNEL')]
        )
        self.discord_bot.loop.create_task(self.bot.start())
        self.bot.command(name="ping")(self.twitch_ping)
        self.bot.command(name="stats")(self.twitch_stats)
        self.bot.listen("event_message")(self.event_message)

    # TwitchIO event
    async def event_message(self, ctx):
        if not ctx.author.is_mod or not ctx.content.startswith(os.getenv('BOT_PREFIX')):
            return
        print(ctx.author.name + ": " + ctx.content)
        await self.bot.handle_commands(ctx)

    async def twitch_ping(self, ctx):
        'Ping the bot to check if it\'s online'
        await ctx.send("pong!")

    async def twitch_stats(self, ctx):
        'Get the stats from the most recent game'
        bot = None
        await val.deathmatchCheck(bot)
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

def setup(discord_bot):
    discord_bot.add_cog(Twitch(discord_bot))