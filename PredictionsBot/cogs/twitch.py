import aiohttp.client_exceptions as aioerror
import PredictionsBot.valorant as val
from PredictionsBot.config import Config
from twitchio.ext import commands as commands

from discord.ext import commands as discord_commands


class Twitch(discord_commands.Cog):
    def __init__(self, bot):
        self.discord_bot = bot
        self.twitchbot = commands.Bot(
            token=self.discord_bot.TMI_TOKEN,
            client_secret=self.discord_bot.CLIENT_ID,
            prefix=self.discord_bot.BOT_PREFIX,
            initial_channels=self.discord_bot.CHANNEL,
            case_insensitive=True
        )
        self.twitchbot.loop.create_task(
            self.discord_bot.start(self.discord_bot.TOKEN))
        self.twitchbot.command(name="ping")(self.twitch_ping)
        self.twitchbot.command(name="stats")(self.twitch_stats)
        self.twitchbot.run()

    async def twitch_ping(self, ctx):
        'Ping the bot to check if it\'s online'
        if ctx.author.is_mod or ctx.author.name == self.discord_bot.TWITCH_BOT_OWNER:
            await ctx.send("pong!")

    async def twitch_stats(self, ctx):
        'Get the stats from the most recent game'
        if ctx.author.is_mod or ctx.author.name == self.discord_bot.TWITCH_BOT_OWNER:
            try:
                await val.gamemode_check(self.discord_bot, Config.USERNAME, Config.TAG)
            except aioerror.CommandInvokeError:
                await ctx.send("API down Sadge")
            if val.DATA == None:
                if val.DEATHMATCH == False:
                    if val.HAS_WON is not None:
                        if val.HAS_WON is True:
                            result = "Yes"
                        else:
                            result = "No"
                    else:
                        # Still not confident in the val.HAS_WON logic for when draws happen
                        # So lets keep this here just in case
                        if val.ROUNDS_WON > val.ROUNDS_LOST:
                            result = "Yes"
                        elif val.ROUNDS_WON < val.ROUNDS_LOST:
                            result = "No"
                        elif val.ROUNDS_WON == val.ROUNDS_LOST:
                            result = "Draw"
                    await ctx.send(
                        f"Map: {val.MAP_PLAYED} | "
                        f"{val.GAME_TIME} | "
                        f"rounds played: {val.ROUNDS_PLAYED} | "
                        f"rounds won: {val.ROUNDS_WON} | "
                        f"rounds lost: {val.ROUNDS_LOST} | "
                        f"K/D/A: {val.KDA} | "
                        f"Did they win? {result}"
                    )
                else:
                    await ctx.send(
                        f"{val.GAME_TIME} | "
                        f"K/D/A: {val.KDA}"
                    )
            else:
                await ctx.send(f"API Error: {val.DATA}")


def setup(discord_bot):
    discord_bot.add_cog(Twitch(discord_bot))
