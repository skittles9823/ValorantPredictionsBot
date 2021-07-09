import json

import aiohttp.client_exceptions as aioerror
import PredictionsBot.valorant as val
from PredictionsBot.__main__ import bot

import discord
from discord.ext import commands


class Discord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Ping the bot to see if it's online
    @commands.command(name='ping', help='ping the bot to see if it\'s alive')
    @commands.check_any(commands.is_owner(), commands.has_any_role(*bot.ROLES))
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round (self.bot.latency * 1000)} ms')

    # Get the stats from the most recent game as well as the K/D/A from all players on the players team
    @commands.command(name='stats', help=f'get the stats from the players last match: {bot.BOT_PREFIX}stats | {bot.BOT_PREFIX}stats {{username}}')
    @commands.max_concurrency(1, wait=True)
    @commands.check_any(commands.is_owner(), commands.has_any_role(*bot.ROLES))
    async def stats(self, ctx, arg=None):
        account_names = ""
        if arg is not None:
            try:
                arg = arg.lower()
                with open('accounts.json') as json_file:
                    account_data = json.load(json_file)
                    for account in account_data['data']['accounts']:
                        account_names += f"{account['username']}, "
                        if arg in account['username'].lower():
                            bot.PUUID = account['puuid']
                            bot.USERNAME = account['username']
                            bot.REGION = account['region']
                if not arg in account_names.lower():
                    account_names = account_names[:-2]
                    await ctx.send(f"Please use a valid account after {bot.BOT_PREFIX}stats\n"
                                   f"Valid names are: {account_names}.")
                    return
            except AttributeError:
                pass
            except TypeError:
                pass
        try:
            await val.gamemode_check(self.bot)
        except aioerror.CommandInvokeError:
            await ctx.send(f"API down {discord.utils.get(self.bot.emojis, name='Sadge')}")
        if val.DATA == None:
            embed = discord.Embed(
                title=f"{val.MAP_PLAYED} {val.MODE} Results", color=0x00aaff)
            embed.set_author(name="ValorantPredictionsBot",
                             url="https://github.com/skittles9823/ValorantPredictionsBot")
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
                username = bot.USERNAME
                embed.add_field(name="Rounds Played:",
                                value=val.ROUNDS_PLAYED, inline=True)
                embed.add_field(name="Rounds Won:",
                                value=val.ROUNDS_WON, inline=True)
                embed.add_field(name="Rounds Lost:",
                                value=val.ROUNDS_LOST, inline=True)
                embed.add_field(name="Match Start Time:",
                                value=val.GAME_TIME, inline=True)
                embed.add_field(name="K/D/A:", value=val.KDA, inline=True)
                embed.add_field(name="Did they win?",
                                value=result, inline=True)
                embed.add_field(name="MatchMVP:",
                                value=val.MATCH_MVP, inline=True)
                embed.add_field(name=f"{username}'s team:",
                                value=val.TEAM_PLAYERS, inline=False)
                embed.add_field(name="Opponents team:",
                                value=val.OPPONENT_PLAYERS, inline=False)
                await ctx.send(embed=embed)
            else:
                if val.KILLS == 40:
                    result = "Yes"
                else:
                    result = "No"
                embed.add_field(name="Match Start Time:",
                                value=val.GAME_TIME, inline=True)
                embed.add_field(name="K/D/A:", value=val.KDA, inline=True)
                embed.add_field(name="Did they win?",
                                value=result, inline=True)
                embed.add_field(name="Players:",
                                value=val.ALL_PLAYERS, inline=False)
                await ctx.send(embed=embed)
        else:
            await ctx.send(f"API Error {discord.utils.get(self.bot.emojis, name='Sadge')}: {val.DATA}")


def setup(discord_bot):
    discord_bot.add_cog(Discord(discord_bot))
