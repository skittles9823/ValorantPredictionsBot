import aiohttp
import discord

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


async def gamemode_check(bot):
    puuid = bot.PUUID
    region = bot.REGION
    username = bot.USERNAME.lower()
    global DATA, resp_error
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(
            f"https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/{region}/{puuid}"
        ) as response:
            try:
                json_data = await response.json()
            except:
                DATA = f"Cloudflare: API Server Down"
                resp_error = response
                return DATA, resp_error
    global MODE
    try:
        data = json_data["data"][0]["data"]
    except KeyError:
        try:
            data = json_data["data"][0]
        except KeyError:
            DATA = json_data["message"]
            return DATA
    try:
        MODE = data["metadata"]["mode"]
    except KeyError:
        MODE = "Unknown"
    global DEATHMATCH
    if MODE.lower() in ["competitive", "unrated", "custom game", "unknown"]:
        DEATHMATCH = False
        await get_match_info(bot, data, username)
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
            MODE,
            MATCH_MVP
        )
    elif MODE.lower() == "deathmatch":
        DEATHMATCH = True
        await get_deathmatch_info(bot, data, username, puuid)
        return DEATHMATCH, GAME_TIME, KDA, MODE


# Get the full json response for the most recent match played
async def get_match_info(bot, data, username):
    global MAP_PLAYED
    global GAME_TIME
    global TEAM_PLAYERS
    global OPPONENT_PLAYERS
    global ROUNDS_PLAYED
    global ROUNDS_WON
    global ROUNDS_LOST
    global KDA
    global HAS_WON
    global MATCH_MVP
    players = data["players"]
    user = next(d for d in players["all_players"]
                if username in d["name"].lower())
    team = user["team"].lower()
    opponent_team = "red" if team == "blue" else "blue"
    OPPONENT_PLAYERS = ""
    TEAM_PLAYERS = ""
    mvp_team = max(players[team], key=lambda ev: ev["stats"]["score"])
    mvp_opponent = max(players[opponent_team],
                       key=lambda ev: ev["stats"]["score"])
    if mvp_team["stats"]["score"] > mvp_opponent["stats"]["score"]:
        MATCH_MVP = mvp_team["name"]
    else:
        MATCH_MVP = mvp_opponent["name"]
    ROUNDS_PLAYED = int(data["metadata"]["rounds_played"])
    MAP_PLAYED = str(data["metadata"]["map"])
    rank_emote = ""
    for player in players[team]:
        acs = int(player["stats"]["score"]) // ROUNDS_PLAYED
        try:
            agent_emote = str(player["character"])
            if agent_emote == "KAY/O":
                agent_emote = "KAYO"
        except KeyError:
            agent_emote = "modCheck"
        agent_emote = (
            "" if bot is None else discord.utils.get(
                bot.emojis, name=str(agent_emote))
        )
        if agent_emote is None:
            agent_emote = discord.utils.get(bot.emojis, name="modCheck")
        if MODE.lower() == "competitive":
            rank = str(player["currenttier_patched"]).replace(' ', '')
            rank_emote = (
                "" if bot is None else discord.utils.get(
                    bot.emojis, name=str(rank))
            )
            if rank_emote is None:
                rank_emote = ""
        player_kda = f'{player["stats"]["kills"]}/{player["stats"]["deaths"]}/{player["stats"]["assists"]}'
        name = player["name"]
        TEAM_PLAYERS += (
            f'{agent_emote}{rank_emote} `{name :<15} {player_kda :>10} {acs:>10} `\n'
        )
    TEAM_PLAYERS = TEAM_PLAYERS.rstrip()
    team_players_split = TEAM_PLAYERS.split("\n")
    team_players_split = team_players_split[:5]
    team_players_split.sort(key=lambda x: int(
        x.rsplit(" ", 2)[1]), reverse=True)
    TEAM_PLAYERS = "\n".join(team_players_split)
    for player in players[opponent_team]:
        acs = int(player["stats"]["score"]) // ROUNDS_PLAYED
        try:
            agent_emote = str(player["character"])
            if agent_emote == "KAY/O":
                agent_emote = "KAYO"
        except KeyError:
            agent_emote = "modCheck"
        agent_emote = (
            "" if bot is None else discord.utils.get(
                bot.emojis, name=str(agent_emote))
        )
        if agent_emote is None:
            agent_emote = discord.utils.get(bot.emojis, name="modCheck")
        if MODE.lower() == "competitive":
            rank = str(player["currenttier_patched"]).replace(' ', '')
            rank_emote = (
                "" if bot is None else discord.utils.get(
                    bot.emojis, name=str(rank))
            )
            if rank_emote is None:
                rank_emote = ""
        player_kda = f'{player["stats"]["kills"]}/{player["stats"]["deaths"]}/{player["stats"]["assists"]}'
        name = player["name"]
        OPPONENT_PLAYERS += (
            f'{agent_emote}{rank_emote} `{name :<15} {player_kda :>10} {acs:>10} `\n'
        )
    OPPONENT_PLAYERS = OPPONENT_PLAYERS.rstrip()
    opponent_players_split = OPPONENT_PLAYERS.split("\n")
    opponent_players_split = opponent_players_split[:5]
    opponent_players_split.sort(key=lambda x: int(
        x.rsplit(" ", 2)[1]), reverse=True)
    OPPONENT_PLAYERS = "\n".join(opponent_players_split)
    ROUNDS_WON = data["teams"][team]["rounds_won"]
    ROUNDS_LOST = data["teams"][team]["rounds_lost"]
    HAS_WON = None
    if data["teams"][team]["has_won"] is True:
        HAS_WON = True
    elif data["teams"][team]["has_won"] is False:
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
        score = int(player["stats"]["score"])
        try:
            agent_emote = str(player["character"])
            if agent_emote == "KAY/O":
                agent_emote = "KAYO"
        except KeyError:
            agent_emote = "modCheck"
        agent_emote = "" if bot is None else discord.utils.get(
            bot.emojis, name=str(agent_emote))

        player_kda = f'{player["stats"]["kills"]}/{player["stats"]["deaths"]}/{player["stats"]["assists"]}'
        name = player["name"]
        ALL_PLAYERS += (
            f'{agent_emote} '
            f'`{name :<15} {player_kda :>10} {score:>10} `\n'
        )
    ALL_PLAYERS = ALL_PLAYERS.rstrip()
    split = ALL_PLAYERS.split("\n")
    split = split[0:14]
    split.sort(key=lambda x: int(x.rsplit(" ", 2)[1]), reverse=True)
    ALL_PLAYERS = "\n".join(split)
    return MAP_PLAYED, GAME_TIME, ALL_PLAYERS, KDA, KILLS
