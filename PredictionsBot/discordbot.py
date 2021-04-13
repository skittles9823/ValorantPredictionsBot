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
    await ctx.send("pong!")


# If streamer changes accounts sometimes, change these so you can have and change accounts on the fly
# without having to restart the bot after changing the config
@commands.max_concurrency(1, wait=True)
@bot.command(name='account', help='temp')
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
@commands.max_concurrency(1, wait=True)
@bot.command(name='stats', help='Get the stats of the players last match')
@commands.has_any_role('predictions', 'Twitch Moderator', 'Moderators')
async def stats(ctx):
    await ctx.send("`Please wait up to 10 seconds for me to retrieve the match info.`")
    try:
        deathmatch = val.getLatestMatchInfo(bot)
    except ValueError:
        await ctx.send("Server down :monkaW:")
        return
    if deathmatch[0] == False:
        deathmatch, gameTime, teamPlayers, opponentPlayers, roundsPlayed, roundsWon, roundsLost, KDA = val.getLatestMatchInfo(bot)
        if roundsWon > roundsLost:
            result = "Yes"
        elif roundsWon < roundsLost:
            result = "No"
        elif roundsWon == roundsLost:
            result = "Draw"
        username = os.getenv('USERNAME')
        embed=discord.Embed(title="Game Results", color=0x00aaff)
        embed.set_author(name="ValorantPredictionsBot", url="https://github.com/skittles9823/ValorantPredictionsBot")
        embed.add_field(name="Match Start Time:", value=gameTime, inline=True)
        embed.add_field(name="Rounds Played:", value=roundsPlayed, inline=True)
        embed.add_field(name="Rounds Won:", value=roundsWon, inline=True)
        embed.add_field(name="Rounds Lost:", value=roundsLost, inline=True)
        embed.add_field(name="K/D/A:", value=KDA, inline=True)
        embed.add_field(name="Did they win?", value=result, inline=True)
        embed.add_field(name=f"{username}'s team:", value=teamPlayers, inline=False)
        embed.add_field(name="Opponents team:", value=opponentPlayers, inline=False)
        await ctx.send(embed=embed)
    else:
        deathmatch, gameTime, KDA = val.getLatestMatchInfo(bot)
        await ctx.send(
            f"{gameTime}\n"
            f"K/D/A: {KDA}"
        )


bot.run(TOKEN)
