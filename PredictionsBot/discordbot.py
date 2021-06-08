import os
import discord
import json
import PredictionsBot.valorant as val
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv("config.env")


TOKEN = str(os.getenv('DISCORD_TOKEN'))
DEBUG = str(os.getenv('DEBUG')).lower()
bot = commands.Bot(command_prefix=os.getenv('BOT_PREFIX'))

if DEBUG != "true":
    # Don't have a panic attack if someone runs a command the bot doesn't have
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.errors.MissingRole):
            pass


# Ping the bot to see if it's online
@bot.command(name='ping', help='ping the bot to see if it\'s alive')
@commands.has_any_role('predictions', 'Twitch Moderator', 'Moderators')
async def ping(ctx):
    await ctx.send(f'Pong! {round (bot.latency * 1000)} ms')


# If streamer changes accounts sometimes, change these so you can have and change accounts on the fly
# without having to restart the bot after changing the config
@bot.command(name='account', help='Switch players the bot is getting stats for')
@commands.max_concurrency(1, wait=True)
@commands.has_any_role('predictions', 'Twitch Moderator', 'Moderators')
async def account(ctx, arg):
    with open('accounts.json') as json_file:
        json_data = json.load(json_file)
        for accounts in json_data['data']['accounts']:
            if arg.lower() in accounts['username'].lower():
                os.environ["discordArgs"] = "True"
                os.environ["PUUID"] = accounts['puuid']
                os.environ["USERNAME"] = accounts['username']
    username = os.getenv('USERNAME')
    await ctx.send(f"Account is set to {username}")


# Get the stats from the most recent game as well as the K/D/A from all players on the players team
@bot.command(name='stats', help='Get the stats of the players last match')
@commands.max_concurrency(1, wait=True)
@commands.has_any_role('predictions', 'Twitch Moderator', 'Moderators')
async def stats(ctx):
    val.deathmatchCheck(bot)
    if val.deathmatch == False:
        if val.roundsWon > val.roundsLost:
            result = "Yes"
        elif val.roundsWon < val.roundsLost:
            result = "No"
        elif val.roundsWon == val.roundsLost:
            result = "Draw"
        username = os.getenv('USERNAME')
        embed=discord.Embed(title=f"{val.mapPlayed} Game Results", color=0x00aaff)
        embed.set_author(name="ValorantPredictionsBot", url="https://github.com/skittles9823/ValorantPredictionsBot")
        embed.add_field(name="Rounds Played:", value=val.roundsPlayed, inline=True)
        embed.add_field(name="Rounds Won:", value=val.roundsWon, inline=True)
        embed.add_field(name="Rounds Lost:", value=val.roundsLost, inline=True)
        embed.add_field(name="Match Start Time:", value=val.gameTime, inline=True)
        embed.add_field(name="K/D/A:", value=val.KDA, inline=True)
        embed.add_field(name="Did they win?", value=result, inline=True)
        embed.add_field(name=f"{username}'s team:", value=val.teamPlayers, inline=False)
        embed.add_field(name="Opponents team:", value=val.opponentPlayers, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(
            f"{val.gameTime}\n"
            f"K/D/A: {val.KDA}"
        )


bot.run(TOKEN)
