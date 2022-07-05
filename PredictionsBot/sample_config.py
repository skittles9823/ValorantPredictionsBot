class Config(object):
    # Global
    BOT_PREFIX = "*"
    DEBUG = False

    # Twitch stuff
    # If you don't need a twitch bot you may comment out these lines and just fill in the Discord and Valorant variables.
    TMI_TOKEN = "oauth:"
    CLIENT_ID = ""
    BOT_NICK = ""
    CHANNEL = ['']
    # Name of the bot owner
    TWITCH_BOT_OWNER = ""

    # Discord stuff
    # My token
    DISCORD_TOKEN = ""

    # Valorant stuff
    # Used to find which team the specified player is on
    USERNAME = "Hiko"
    # Regions can be na, ap, eu, or kr
    REGION = "na"
    # Hiko's PUUID
    PUUID = "966186a2-fa1e-5445-b1c3-ab25f210f3e3"
