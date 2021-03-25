import os
import discord
from discord.ext import commands
import PredictionsBot.valorant as val
from dotenv import load_dotenv

load_dotenv("config.env")


TOKEN = str(os.getenv('DISCORD_TOKEN'))
DEBUG = str(os.getenv('DEBUG')).lower()
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


# If streamer changes accounts sometimes, change these so you can have and change accounts on the fly
# without having to restart the bot after changing the config
@bot.command(name='account', help='temp')
@commands.has_role('predictions')
async def account(ctx, arg):
    if arg == "main":
        os.environ["discordArgs"] = "True"
        os.environ["PUUID"] = "966186a2-fa1e-5445-b1c3-ab25f210f3e3"
        os.environ["USERNAME"] = "Hiko"
        await ctx.send("Set account to Hiko")
        return
    if arg == "hoodie":
        os.environ["discordArgs"] = "True"
        os.environ["PUUID"] = "d34d1fce-bc25-55eb-b59a-130839e8a4e2"
        os.environ["USERNAME"] = "Hoodie Seller"
        await ctx.send("Set account to Hoodie Seller")
        return


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
        username = os.getenv('USERNAME')
        embed=discord.Embed(title="Game Results", color=0x00aaff)
        embed.add_field(name="Total Time: ", value=f"{gameTime}", inline=False)
        embed.add_field(name="Rounds Played:", value=f"{roundsPlayed}", inline=False)
        embed.add_field(name="Rounds Won:", value=f"{roundsWon}", inline=False)
        embed.add_field(name="Rounds Lost:", value=f"{roundsLost}", inline=False)
        embed.add_field(name="K/D/A:", value=f"{KDA}", inline=False)
        embed.add_field(name="Did they win?", value=f"{result}", inline=False)
        embed.add_field(name=f"{username}'s team:", value=f"{teamPlayers}", inline=False)
        embed.add_field(name="Opponents team:", value=f"{opponentPlayers}", inline=False)
        await ctx.send(embed=embed)
    else:
        deathmatch, gameTime, KDA = val.getLatestMatchInfo()
        await ctx.send(
            f"{gameTime}\n"
            f"K/D/A: {KDA}"
        )


bot.run(TOKEN)
