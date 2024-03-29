import aiohttp.client_exceptions as aioerror
import PredictionsBot.valorant as val
from PredictionsBot.__main__ import bot
from PredictionsBot.config import Config

import discord
from discord import option
from discord.ext import commands

bot = discord.Bot()


class Discord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Ping the bot to see if it's online

    @commands.slash_command()
    @discord.default_permissions(
        manage_messages=True,
        ban_members=True,
    )
    async def ping(self, ctx: discord.ApplicationContext):
        await ctx.respond(f'Pong! {round (self.bot.latency * 1000)} ms')

    @commands.slash_command()
    @discord.default_permissions(
        manage_messages=True,
        ban_members=True,
    )
    @option("code", description="crosshair code")
    async def crosshair(self, ctx: discord.ApplicationContext, code: str):
        embed = discord.Embed()
        embed.set_image(
            url=f"https://api.henrikdev.xyz/valorant/v1/crosshair/generate?id={code}"
        )
        embed.add_field(name="Import Code:", value=f"{code}", inline=False)
        await ctx.respond(embed=embed)

    # Get the stats from the most recent game as well as the K/D/A from all players on the players team
    @commands.slash_command()
    @discord.default_permissions(
        manage_messages=True,
        ban_members=True,
    )
    @option("username", description="username, optional.", default=Config.USERNAME)
    @option("tag", description="tag, optional.", default=Config.TAG)
    async def stats(self, ctx: discord.ApplicationContext, username: str, tag: str):
        await ctx.respond("Processing...")
        try:
            await val.gamemode_check(self.bot, username, tag)
        except aioerror.CommandInvokeError:
            await ctx.edit(f"API down {discord.utils.get(self.bot.emojis, name='Sadge')}")
        if val.DATA == None:
            embed = discord.Embed(
                title=f"{val.MAP_PLAYED} {val.MODE} Results",
                color=discord.Color.blue()
            )
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
                username = val.USERNAME
                embed.add_field(name="Rounds Played:",
                                value=f"{val.ROUNDS_PLAYED}",
                                inline=True)
                embed.add_field(name="Rounds Won:",
                                value=f"{val.ROUNDS_WON}",
                                inline=True)
                embed.add_field(name="Rounds Lost:",
                                value=f"{val.ROUNDS_LOST}",
                                inline=True)
                embed.add_field(name="Match Start Time:",
                                value=f"{val.GAME_TIME}",
                                inline=True)
                embed.add_field(name="K/D/A:",
                                value=f"{val.KDA}",
                                inline=True)
                embed.add_field(name="Did they win?",
                                value=f"{result}",
                                inline=True)
                embed.add_field(name="MatchMVP:",
                                value=f"{val.MATCH_MVP}",
                                inline=True)
                embed.add_field(name=f"{username}'s team:",
                                value=f"{val.TEAM_PLAYERS}",
                                inline=False)
                embed.add_field(name="Opponents team:",
                                value=f"{val.OPPONENT_PLAYERS}",
                                inline=False)
            else:
                if val.KILLS == 40:
                    result = "Yes"
                else:
                    result = "No"
                embed.add_field(name="Match Start Time:",
                                value=f"{val.GAME_TIME}",
                                inline=True)
                embed.add_field(name="K/D/A:",
                                value=f"{val.KDA}",
                                inline=True)
                embed.add_field(name="Did they win?",
                                value=f"{result}",
                                inline=True)
                embed.add_field(name="Players:",
                                value=f"{val.ALL_PLAYERS}",
                                inline=False)
            embed.set_author(name="ValorantPredictionsBot",
                             url="https://github.com/skittles9823/ValorantPredictionsBot")
            await ctx.edit(embed=embed)
        else:
            await ctx.edit(f"API Error {discord.utils.get(self.bot.emojis, name='Sadge')}: {val.DATA}")
            await ctx.edit(f"{val.resp_error}")


def setup(bot):
    bot.add_cog(Discord(bot))
