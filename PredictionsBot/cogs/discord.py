import json
import os

import aiohttp.client_exceptions as aioerror
import PredictionsBot.valorant as val

import discord
from discord.ext import commands


class Discord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', help='ping the bot to see if it\'s alive')
    # Ping the bot to see if it's online
    @commands.has_any_role('predictions', 'Twitch Moderator', 'Moderators')
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round (self.bot.latency * 1000)} ms')

    # If streamer changes accounts sometimes, change these so you can have and change accounts on the fly
    # without having to restart the bot after changing the config
    @commands.command(name='account', help='Switch players the bot is getting stats for')
    @commands.max_concurrency(1, wait=True)
    @commands.has_any_role('predictions', 'Twitch Moderator', 'Moderators')
    async def account(self, ctx, arg):
        with open('accounts.json') as json_file:
            json_data = json.load(json_file)
            for accounts in json_data['data']['accounts']:
                if arg.lower() in accounts['username'].lower():
                    os.environ["discordArgs"] = "True"
                    os.environ["PUUID"] = accounts['puuid']
                    os.environ["USERNAME"] = accounts['username']
                    os.environ["REGION"] = accounts['region']
        username = os.getenv('USERNAME')
        await ctx.send(f"Account is set to {username}")

    # Get the stats from the most recent game as well as the K/D/A from all players on the players team
    @commands.command(name='stats', help='Get the stats of the players last match')
    @commands.max_concurrency(1, wait=True)
    @commands.has_any_role('predictions', 'Twitch Moderator', 'Moderators')
    async def stats(self, ctx):
        try:
            await val.gamemode_check(self.bot)
        except aioerror.CommandInvokeError:
            await ctx.send(f"API down {discord.utils.get(self.bot.emojis, name='Sadge')}")
        embed = discord.Embed(
            title=f"{val.MAP_PLAYED} {val.MODE} Results", color=0x00aaff)
        embed.set_author(name="ValorantPredictionsBot",
                         url="https://github.com/skittles9823/ValorantPredictionsBot")
        if val.DEATHMATCH == False:
            # data["teams"][team]["has_won"] was removed previously as it didn't work in custom games
            # looks like the functionality is back, but I'd like to wait to test draws before adding it back.
            # if val.HAS_WON is not None:
            #    if val.HAS_WON == "true":
            #        result = "Yes"
            #    else:
            #        result = "No"
            #
            # I believe the val.ROUNDS_WON/val.ROUNDS_LOST logic won't work if a team surrenders when they're winning
            # thankfully that is a rare occurance so it's unlikely to happen.
            if val.ROUNDS_WON > val.ROUNDS_LOST:
                result = "Yes"
            elif val.ROUNDS_WON < val.ROUNDS_LOST:
                result = "No"
            elif val.ROUNDS_WON == val.ROUNDS_LOST:
                result = "Draw"
            username = os.getenv('USERNAME')
            embed.add_field(name="Rounds Played:",
                            value=val.ROUNDS_PLAYED, inline=True)
            embed.add_field(name="Rounds Won:",
                            value=val.ROUNDS_WON, inline=True)
            embed.add_field(name="Rounds Lost:",
                            value=val.ROUNDS_LOST, inline=True)
            embed.add_field(name="Match Start Time:",
                            value=val.GAME_TIME, inline=True)
            embed.add_field(name="K/D/A:", value=val.KDA, inline=True)
            embed.add_field(name="Did they win?", value=result, inline=True)
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
            embed.add_field(name="Did they win?", value=result, inline=True)
            embed.add_field(name="Players:",
                            value=val.ALL_PLAYERS, inline=False)
            await ctx.send(embed=embed)


def setup(discord_bot):
    discord_bot.add_cog(Discord(discord_bot))
