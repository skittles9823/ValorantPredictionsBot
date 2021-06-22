import math
import os

import aiohttp
import discord
from dotenv import load_dotenv

MODE = None
DEATHMATCH = None
MAP_PLAYED = None
GAME_TIME = None
KILLS = None
KDA = None
ALL_PLAYERS = None
TEAM_PLAYERS = None
OPPONENT_PLAYERS = None

ROUNDS_PLAYED = None
ROUNDS_WON = None
ROUNDS_LOST = None
HAS_WON = None
OPPONENT_PLAYERS = None

DATA = None

if os.getenv("discordArgs") != "True":
    load_dotenv("config.env")


async def gamemode_check(bot):
    puuid = os.getenv("PUUID")
    region = os.getenv("REGION")
    username = os.getenv("USERNAME").lower()
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/{region}/{puuid}"
        ) as response:
            json_data = await response.json()
    global MODE
    try:
        data = json_data["data"][0]["data"]
    except KeyError:
        try:
            data = json_data["data"][0]
        except KeyError:
            global DATA
            DATA = json_data["message"]
            return DATA
    MODE = data["metadata"]["mode"]
    global DEATHMATCH
    if MODE.lower() in ["competitive", "unrated", "custom game"]:
        DEATHMATCH = False
        await get_match_info(bot, data, username, puuid)
        return (
            DEATHMATCH,
            MAP_PLAYED,
            GAME_TIME,
            TEAM_PLAYERS,
            OPPONENT_PLAYERS,
            ROUNDS_PLAYED,
            ROUNDS_WON,
            ROUNDS_LOST,
            KDA,
            HAS_WON,
            MODE
        )
    elif MODE.lower() == "deathmatch":
        DEATHMATCH = True
        await get_deathmatch_info(bot, data, username, puuid)
        return DEATHMATCH, GAME_TIME, KDA, MODE


# Get the full json response for the most recent match played
async def get_match_info(bot, data, username, puuid):
    global MAP_PLAYED
    global GAME_TIME
    global TEAM_PLAYERS
    global OPPONENT_PLAYERS
    global ROUNDS_PLAYED
    global ROUNDS_WON
    global ROUNDS_LOST
    global KDA
    players = data["players"]
    user = next(d for d in players["all_players"]
                if username in d["name"].lower())
    team = user["team"].lower()
    if team != puuid:
        opponent_team = "red" if team == "blue" else "blue"
        OPPONENT_PLAYERS = ""
        TEAM_PLAYERS = ""
        mvp_team = max(players[team], key=lambda ev: ev["stats"]["score"])
        mvp_opponent = max(players[opponent_team],
                           key=lambda ev: ev["stats"]["score"])
        ROUNDS_PLAYED = int(data["metadata"]["rounds_played"])
        MAP_PLAYED = str(data["metadata"]["map"])
        rank_emote = ""
        for player in players[team]:
            match_mvp = ""
            if (
                player["name"] == mvp_team["name"]
                and mvp_team["stats"]["score"] > mvp_opponent["stats"]["score"]
            ):
                match_mvp = "**"
            acs = int(player["stats"]["score"]) / ROUNDS_PLAYED
            acs = math.floor(acs)
            try:
                agent = str(player["character"])
            except KeyError:
                agent = "modCheck"
            agent_emote = (
                "" if bot is None else discord.utils.get(
                    bot.emojis, name=str(agent))
            )
            if MODE.lower() == "competitive":
                rank = str(player["currenttier_patched"]).replace(' ', '')
                rank_emote = (
                    "" if bot is None else discord.utils.get(
                        bot.emojis, name=str(rank))
                )
                if rank_emote is None:
                    rank_emote = ""
            TEAM_PLAYERS += (
                f'{match_mvp}{agent_emote}{rank_emote} {player["name"]}{match_mvp}: '
                f'{player["stats"]["kills"]}/'
                f'{player["stats"]["deaths"]}/'
                f'{player["stats"]["assists"]} ACS: {acs}\n'
            )
        TEAM_PLAYERS = TEAM_PLAYERS.rstrip()
        team_players_split = TEAM_PLAYERS.split("\n")
        team_players_split = team_players_split[:5]
        team_players_split.sort(key=lambda x: int(
            x.rsplit(" ", 1)[1]), reverse=True)
        TEAM_PLAYERS = "\n".join(team_players_split)
        for player in players[opponent_team]:
            match_mvp = ""
            if (
                player["name"] == mvp_opponent["name"]
                and mvp_opponent["stats"]["score"] > mvp_team["stats"]["score"]
            ):
                match_mvp = "**"
            acs = int(player["stats"]["score"]) / ROUNDS_PLAYED
            acs = math.floor(acs)
            try:
                agent = str(player["character"])
            except KeyError:
                agent = "modCheck"
            emote = (
                "" if bot is None else discord.utils.get(
                    bot.emojis, name=str(agent))
            )
            if MODE.lower() == "competitive":
                rank = str(player["currenttier_patched"]).replace(' ', '')
                rank_emote = (
                    "" if bot is None else discord.utils.get(
                        bot.emojis, name=str(rank))
                )
                if rank_emote is None:
                    rank_emote = ""
            OPPONENT_PLAYERS += (
                f'{match_mvp}{emote}{rank_emote} {player["name"]}{match_mvp}: '
                f'{player["stats"]["kills"]}/'
                f'{player["stats"]["deaths"]}/'
                f'{player["stats"]["assists"]} ACS: {acs}\n'
            )
        OPPONENT_PLAYERS = OPPONENT_PLAYERS.rstrip()
        opponent_players_split = OPPONENT_PLAYERS.split("\n")
        opponent_players_split = opponent_players_split[0:5]
        opponent_players_split.sort(key=lambda x: int(
            x.rsplit(" ", 1)[1]), reverse=True)
        OPPONENT_PLAYERS = "\n".join(opponent_players_split)
        ROUNDS_WON = 0
        ROUNDS_LOST = 0
        for rounds in data["rounds"]:
            if rounds["winning_team"].lower() == team:
                ROUNDS_WON += 1
            else:
                ROUNDS_LOST += 1
    if data["teams"][team]["has_won"] == "true":
        HAS_WON = True
    else:
        HAS_WON = False
    GAME_TIME = str(data["metadata"]["game_start_patched"])
    _kills = int(user["stats"]["kills"])
    deaths = int(user["stats"]["deaths"])
    assists = int(user["stats"]["assists"])
    KDA = f"{_kills}/{deaths}/{assists}"
    return (
        MAP_PLAYED,
        GAME_TIME,
        TEAM_PLAYERS,
        OPPONENT_PLAYERS,
        ROUNDS_PLAYED,
        ROUNDS_WON,
        ROUNDS_LOST,
        KDA,
        HAS_WON
    )


async def get_deathmatch_info(bot, data, username, puuid):
    global MAP_PLAYED
    global GAME_TIME
    global ALL_PLAYERS
    global KILLS
    global KDA
    players = data["players"]
    user = next(d for d in players["all_players"]
                if username in d["name"].lower())

    deaths = int(user["stats"]["deaths"])
    assists = int(user["stats"]["assists"])

    GAME_TIME = str(data["metadata"]["game_start_patched"])
    KILLS = int(user["stats"]["kills"])
    KDA = f"{KILLS}/{deaths}/{assists}"
    MAP_PLAYED = str(data["metadata"]["map"])

    ALL_PLAYERS = ""
    for player in players["all_players"]:
        winner = ""
        if player["stats"]["kills"] == 40:
            winner = "**"
        score = int(player["stats"]["score"])
        try:
            agent = str(player["character"])
        except KeyError:
            agent = "modCheck"
        emote = "" if bot is None else discord.utils.get(
            bot.emojis, name=str(agent))
        ALL_PLAYERS += (
            f'{winner}{emote} {player["name"]}{winner}: '
            f'{player["stats"]["kills"]}/'
            f'{player["stats"]["deaths"]}/'
            f'{player["stats"]["assists"]} Score: {score}\n'
        )
    ALL_PLAYERS = ALL_PLAYERS.rstrip()
    split = ALL_PLAYERS.split("\n")
    split = split[0:14]
    split.sort(key=lambda x: int(x.rsplit(" ", 1)[1]), reverse=True)
    ALL_PLAYERS = "\n".join(split)
    return MAP_PLAYED, GAME_TIME, ALL_PLAYERS, KDA, KILLS
