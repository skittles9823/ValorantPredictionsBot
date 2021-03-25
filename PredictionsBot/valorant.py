import requests, os
import math

from dotenv import load_dotenv

if os.getenv('discordArgs') != "True":
    load_dotenv("config.env")


# Get the full json response for the most recent match played
def getLatestMatchInfo():
    puuid = os.getenv('PUUID')
    region = os.getenv('REGION')
    username = os.getenv('USERNAME').lower()
    r = requests.get(f'https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/{region}/{puuid}')
    json_data = r.json()
    Players = json_data['data']['matchres'][0]['players']
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
        roundsPlayed = int(json_data['data']['matchres'][0]['metadata']['rounds_played'])
        for players in Players[Team]:
            if players['name'] == mvpTeam['name']:
                if mvpTeam['stats']['score'] > mvpOpponent['stats']['score']:
                    teamPlayers += "**Match MVP** "
                else:
                    teamPlayers += "**Team MVP** "
            acs = int(players['stats']['score']) / roundsPlayed
            acs = math.floor(acs)
            teamPlayers += str(players['name']) + ": " + "KDA: " + str(players['stats']['kills']) + "/" + \
                            str(players['stats']['deaths']) + "/" + str(players['stats']['assists']) + " ACS: " + str(acs) + "\n"
        split = teamPlayers.split('\n')
        split = split[0:5]
        split.sort(key = lambda x: int(x.rsplit(' ',1)[1]), reverse=True)
        teamPlayers = '\n'.join(split)
        for players in Players[opponentTeam]:
            if players['name'] == mvpOpponent['name']:
                if mvpOpponent['stats']['score'] > mvpTeam['stats']['score']:
                    opponentPlayers += "**Match MVP** "
                else:
                    opponentPlayers += "**Team MVP** "
            acs = int(players['stats']['score']) / roundsPlayed
            acs = math.floor(acs)
            opponentPlayers += str(players['name']) + ": " + "KDA: " + str(players['stats']['kills']) + "/" + \
                              str(players['stats']['deaths']) + "/" + str(players['stats']['assists']) + " ACS: " + str(acs) + "\n"
        split = opponentPlayers.split('\n')
        split = split[0:5]
        split.sort(key = lambda x: int(x.rsplit(' ',1)[1]), reverse=True)
        opponentPlayers = '\n'.join(split)
        playerHasWon = str(json_data['data']['matchres'][0]['teams'][Team]['has_won'])
        roundsWon = int(json_data['data']['matchres'][0]['teams'][Team]['rounds_won'])
        roundsLost = int(json_data['data']['matchres'][0]['teams'][Team]['rounds_lost'])
    gameTime = str(json_data['data']['matchres'][0]['metadata']['game_start_patched'])
    Kills = int(User['stats']['kills'])
    Deaths = int(User['stats']['deaths'])
    Assists = int(User['stats']['assists'])
    KDA = f"{Kills}/{Deaths}/{Assists}"
    if Team != puuid:
        deathmatch = False
        return deathmatch, gameTime, teamPlayers, opponentPlayers, roundsPlayed, playerHasWon, roundsWon, roundsLost, KDA
    else:
        deathmatch = True
        return deathmatch, gameTime, KDA
