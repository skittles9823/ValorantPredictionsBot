import requests, os

from dotenv import load_dotenv

load_dotenv("config.env")

puuid = os.getenv('PUUID')
region = os.getenv('REGION')
username = os.getenv('USERNAME').lower()


# Get the full json response for the most recent match played
def getLatestMatchInfo():
    r = requests.get(f'https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/{region}/{puuid}')
    json_data = r.json()
    Players = json_data['data']['matchres'][0]['players']
    User = next(d for d in Players['all_players'] if username in d['name'].lower())
    Team = User['team'].lower()
    if Team == "blue":
        opponentTeam = "red"
    else:
        opponentTeam = "blue"
    opponentPlayers = ""
    teamPlayers = ""
    for players in Players[Team]:
        teamPlayers += str(players['name']) + " " + str(players['stats']['kills']) + "/" + str(players['stats']['deaths']) + "/" + str(players['stats']['assists']) + "\n"
    for players in Players[opponentTeam]:
        opponentPlayers += str(players['name']) + " " + str(players['stats']['kills']) + "/" + str(players['stats']['deaths']) + "/" + str(players['stats']['assists']) + "\n"
    roundsPlayed = int(json_data['data']['matchres'][0]['metadata']['rounds_played'])
    playerHasWon = str(json_data['data']['matchres'][0]['teams'][Team]['has_won'])
    roundsWon = int(json_data['data']['matchres'][0]['teams'][Team]['rounds_won'])
    roundsLost = int(json_data['data']['matchres'][0]['teams'][Team]['rounds_lost'])
    Kills = int(User['stats']['kills'])
    Deaths = int(User['stats']['deaths'])
    Assists = int(User['stats']['assists'])
    KDA = f"{Kills}/{Deaths}/{Assists}"
    return teamPlayers, opponentPlayers, roundsPlayed, playerHasWon, roundsWon, roundsLost, KDA
    