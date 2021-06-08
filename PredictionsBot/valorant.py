import requests, os
import math
import discord
from dotenv import load_dotenv

if os.getenv('discordArgs') != "True":
    load_dotenv("config.env")


def deathmatchCheck(bot):
    puuid = os.getenv('PUUID')
    region = os.getenv('REGION')
    username = os.getenv('USERNAME').lower()
    r = requests.get(f'https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/{region}/{puuid}')
    json_data = r.json()
    try:
        data = json_data['data'][0]['data']
    except KeyError:
        data = json_data['data'][0]
    mode = data['metadata']['mode'].lower()
    global deathmatch
    if mode == "competitive" or mode == "unrated":
        deathmatch = False
        getMatchInfo(bot, data, username, puuid)
        return deathmatch, mapPlayed, gameTime, teamPlayers, opponentPlayers, roundsPlayed, roundsWon, roundsLost, KDA
    elif mode == "deathmatch":
        deathmatch = True
        getDeathmatchInfo(bot, data, username, puuid)
        return deathmatch, gameTime, KDA


# Get the full json response for the most recent match played
def getMatchInfo(bot, data, username, puuid):
    global mapPlayed; global gameTime; global teamPlayers; global opponentPlayers
    global roundsPlayed; global roundsWon; global roundsLost; global KDA
    Players = data['players']
    User = next(d for d in Players['all_players'] if username in d['name'].lower())
    Team = User['team'].lower()
    if Team != puuid:
        if Team == "blue":
            opponentTeam = "red"
        else:
            opponentTeam = "blue"
        opponentPlayers = ""
        teamPlayers = ""
        mvpTeam = max(Players[Team], key=lambda ev: ev['stats']['score'])
        mvpOpponent = max(Players[opponentTeam], key=lambda ev: ev['stats']['score'])
        roundsPlayed = int(data['metadata']['rounds_played'])
        mapPlayed = str(data['metadata']['map'])
        for players in Players[Team]:
            matchMVP = ""
            if players['name'] == mvpTeam['name']:
                if mvpTeam['stats']['score'] > mvpOpponent['stats']['score']:
                    matchMVP = "**"
            acs = int(players['stats']['score']) / roundsPlayed
            acs = math.floor(acs)
            try:
                agent = str(players['character'])
            except KeyError:
                agent = "modCheck"
            if os.getenv('PLATFORM').lower() != "discord":
                emote = None
            else:
                emote = discord.utils.get(bot.emojis, name=str(agent))
            if emote is None:
                emote = ""
            teamPlayers += str(matchMVP) + str(emote) + str(players['name']) + str(matchMVP) + ": " + "KDA: " + str(players['stats']['kills']) + "/" + \
                            str(players['stats']['deaths']) + "/" + str(players['stats']['assists']) + " ACS: " + str(acs) + "\n"
        teamPlayers = teamPlayers.rstrip()
        split = teamPlayers.split('\n')
        split = split[0:5]
        split.sort(key = lambda x: int(x.rsplit(' ',1)[1]), reverse=True)
        teamPlayers = '\n'.join(split)
        for players in Players[opponentTeam]:
            matchMVP = ""
            if players['name'] == mvpOpponent['name']:
                if mvpOpponent['stats']['score'] > mvpTeam['stats']['score']:
                    matchMVP = "**"
            acs = int(players['stats']['score']) / roundsPlayed
            acs = math.floor(acs)
            try:
                agent = str(players['character'])
            except KeyError:
                agent = "modCheck"
            if os.getenv('PLATFORM').lower() != "discord":
                emote = None
            else:
                emote = discord.utils.get(bot.emojis, name=str(agent))
            if emote is None:
                emote = ""
            opponentPlayers += str(matchMVP) + str(emote) + str(players['name']) + str(matchMVP) + ": " + "KDA: " + str(players['stats']['kills']) + "/" + \
                            str(players['stats']['deaths']) + "/" + str(players['stats']['assists']) + " ACS: " + str(acs) + "\n"
        opponentPlayers = opponentPlayers.rstrip()
        split = opponentPlayers.split('\n')
        split = split[0:5]
        split.sort(key = lambda x: int(x.rsplit(' ',1)[1]), reverse=True)
        opponentPlayers = '\n'.join(split)
        roundsWon = 0
        roundsLost = 0
        for rounds in data['rounds']:
            if rounds['winning_team'].lower() == Team:
                roundsWon += 1
            else:
                roundsLost += 1
    mapPlayed = str(data['metadata']['map'])
    gameTime = str(data['metadata']['game_start_patched'])
    Kills = int(User['stats']['kills'])
    Deaths = int(User['stats']['deaths'])
    Assists = int(User['stats']['assists'])
    KDA = f"{Kills}/{Deaths}/{Assists}"
    return mapPlayed, gameTime, teamPlayers, opponentPlayers, roundsPlayed, roundsWon, roundsLost, KDA


def getDeathmatchInfo(bot, data, username, puuid):
    global gameTime; global KDA
    Players = data['players']
    User = next(d for d in Players['all_players'] if username in d['name'].lower())
    Team = User['team'].lower()
    gameTime = str(data['metadata']['game_start_patched'])
    Kills = int(User['stats']['kills'])
    Deaths = int(User['stats']['deaths'])
    Assists = int(User['stats']['assists'])
    KDA = f"{Kills}/{Deaths}/{Assists}"
    return gameTime, KDA
