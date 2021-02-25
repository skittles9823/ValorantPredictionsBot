import requests, os

from dotenv import load_dotenv

load_dotenv("config.env")

token = os.getenv('API_TOKEN')
puuid = os.getenv('PUUID')

headers = {
    'x-api-token': token
    }


# Get the full json response for the most recent match played
def getLatestMatchInfo():
    r = requests.get(f'https://api.henrikdev.xyz/valorant/v2/by-puuid/matches/{puuid}', headers=headers)
    json_data = r.json()
    gameID = str(json_data['matches'][0]['metadata']['gameid'])
    return json_data, gameID
    #Damage = str(json_data['matches'][0]['game']['damagemade'])
    #combatScore = float(json_data['matches'][0]['game']['score'])
    #HS = float(json_data['matches'][0]['game']['headshots'])
    #HSP = int(json_data['matches'][0]['game']['headshotspercentage'])


# Turn json response into data for the bots to read
def stats():
    json_data, gameID = getLatestMatchInfo()
    roundsPlayed = int(json_data['matches'][0]['game']['roundsplayed'])
    roundsWon = int(json_data['matches'][0]['game']['roundswon'])
    roundsLost = int(json_data['matches'][0]['game']['roundslost'])
    KDA = str(json_data['matches'][0]['game']['kda']['kda'])
    KD = float(json_data['matches'][0]['game']['kda']['kd'])
    Kills = str(json_data['matches'][0]['game']['kda']['kills'])
    Deaths = float(json_data['matches'][0]['game']['kda']['deaths'])
    Assists = str(json_data['matches'][0]['game']['kda']['assists'])
    playerHasWon = str(json_data['matches'][0]['metadata']['playerhaswon'])
    return roundsPlayed, roundsWon, roundsLost, KDA, KD, Kills, Deaths, Assists, playerHasWon


# Get some more data if mods need info from every player in the team
def getAllPlayers():
    json_data, gameID = getLatestMatchInfo()
    r = requests.get(f'https://api.henrikdev.xyz/valorant/v2/match/{gameID}')
    json_data = r.json()
    Players = json_data['data']['players']
    Hiko = next(d for d in Players['all_players'] if 'hiko' in d['name'].lower())
    Team = Hiko['team'].lower()
    teamPlayers = ""
    for players in Players[Team]:
        teamPlayers += str(players['name']) + " " + str(players['stats']['kills']) + "/" + str(players['stats']['deaths']) + "/" + str(players['stats']['assists']) + "\n"
    return teamPlayers
