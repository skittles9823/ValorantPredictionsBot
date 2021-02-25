import os
from twitchio.ext import commands
import PredictionsBot.valorant as val
from dotenv import load_dotenv

load_dotenv("config.env")

bot = commands.Bot(
    # set up the bot
    token=os.getenv('TMI_TOKEN'),
    client_secret=os.getenv('CLIENT_ID'),
    nick=os.getenv('BOT_NICK'),
    prefix=os.getenv('BOT_PREFIX'),
    initial_channels=[os.getenv('CHANNEL')]
)


@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"{os.environ['BOT_NICK']} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")


@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'
    # make sure the bot ignores itself and the streamer
    if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
        return
    if not ctx.author.is_mod:
        return
    await bot.handle_commands(ctx)


@bot.command(name='ping')
async def ping(ctx):
    'Ping the bot to check if it\'s online'
    await ctx.send("pong!")


@bot.command(name='stats')
async def stats(ctx):
    'Get the stats from the most recent game'
    await ctx.send("Please wait up to 10 seconds for me to retrieve the match info.")
    roundsPlayed, roundsWon, roundsLost, KDA, KD, Kills, Deaths, Assists, playerHasWon = val.stats()
    result = "no"
    if playerHasWon != "false":
        result = "yes"
    await ctx.send(
        f"{roundsPlayed} rounds played | "
        f"{roundsWon} rounds won | "
        f"{roundsLost} rounds lost | "
        f"Their KDA was {KDA} | "
        f"Their KD was {KD} | "
        f"Did they win? {result}"
    )


# Headshots stats currently not being reported from the v2 endpoint
#@bot.command(name='hs')
#async def test(ctx):
#    await ctx.send("How many headshots: " + str(matchInfo().HS) + " | Headshot%: " + str(matchInfo().HSP) + "%")


bot.run()