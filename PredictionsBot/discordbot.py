import os
from discord.ext import commands
import PredictionsBot.valorant as val
from dotenv import load_dotenv

load_dotenv("config.env")


TOKEN = str(os.getenv('DISCORD_TOKEN'))
DEBUG = str(os.getenv('DEBUG')).lower()
username = os.getenv('USERNAME')
bot = commands.Bot(command_prefix=os.getenv('BOT_PREFIX'))

if DEBUG != "True":
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


# Get the stats from the most recent game as well as the K/D/A from all players on the players team
@bot.command(name='stats', help='Get the stats of the players last match')
@commands.has_role('predictions')
async def stats(ctx):
    await ctx.send("Please wait up to 10 seconds for me to retrieve the match info.")
    try:
        deathmatch = val.getLatestMatchInfo()
    except ValueError:
        await ctx.send("Server down :monkaW:")
        return
    if deathmatch[0] == False:
        deathmatch, gameTime, teamPlayers, opponentPlayers, roundsPlayed, playerHasWon, roundsWon, roundsLost, KDA = val.getLatestMatchInfo()
        result = "No"
        if playerHasWon != "False":
            result = "Yes"
        await ctx.send(
            f"{gameTime}\n"
            f"rounds played: {roundsPlayed}\n"
            f"rounds won: {roundsWon}\n"
            f"rounds lost: {roundsLost}\n"
            f"K/D/A: {KDA}\n"
            f"Did they win? {result}\n\n"
            f"{username}\'s team:\n"
            f"{teamPlayers}\n"
            "Opponents team:\n"
            f"{opponentPlayers}"
        )
    else:
        deathmatch, gameTime, roundsPlayed, KDA = val.getLatestMatchInfo()
        await ctx.send(
            f"{gameTime}\n"
            f"K/D/A: {KDA}"
        )


bot.run(TOKEN)
