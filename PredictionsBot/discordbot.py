import os
from discord.ext import commands
import PredictionsBot.valorant as val
from dotenv import load_dotenv

load_dotenv("config.env")


TOKEN = str(os.getenv('DISCORD_TOKEN'))
bot = commands.Bot(command_prefix='^')


# Don't have a panic attack if someone runs a command the bot doesn't have
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRole):
        pass


# Ping the bot to see if it's online
@bot.command(name='ping', help='ping the bot to see if it\'s alive')
@commands.has_role('predictions')
async def ping(ctx):
    await ctx.send("pong!")


# Get the stats from the most recent game
@bot.command(name='stats', help='Get the stats of the players last match')
@commands.has_role('predictions')
async def stats(ctx):
    await ctx.send("Please wait up to 10 seconds for me to retrieve the match info.")
    roundsPlayed, roundsWon, roundsLost, KDA, KD, Kills, Deaths, Assists, playerHasWon = val.stats()
    result = "no"
    if playerHasWon != "false":
        result = "yes"
    await ctx.send(
        f"{roundsPlayed} rounds played\n"
        f"{roundsWon} rounds won\n"
        f"{roundsLost} rounds lost\n"
        f"Their KDA was {KDA}\n"
        f"Their KD was {KD}\n"
        f"Did they win? {result}"
    )


# Get the stats from the most recent game as well as the K/D/A from all players on the players team
@bot.command(name='allstats', help='Get the stats of the players last match')
@commands.has_role('predictions')
async def stats(ctx):
    await ctx.send("Please wait up to 10 seconds for me to retrieve the match info.")
    roundsPlayed, roundsWon, roundsLost, KDA, KD, Kills, Deaths, Assists, playerHasWon = val.stats()
    teamPlayers = val.getAllPlayers()
    result = "no"
    if playerHasWon != "false":
        result = "yes"
    await ctx.send(
        f"{roundsPlayed} rounds played\n"
        f"{roundsWon} rounds won\n"
        f"{roundsLost} rounds lost\n"
        f"Their KDA was {KDA}\n"
        f"Their KD was {KD}\n"
        f"Did they win? {result}\n\n"
        "Players:\n"
        f"{teamPlayers}"
    )


bot.run(TOKEN)