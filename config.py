import os

from rumble_royale import rumble_royale_config
from pixxie_bot import pixxie_bot_config

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN_NUGGIES_LITTLE_HELPER")

BOT_APP_ID_RUMBLE_ROYALE = rumble_royale_config.BOT_APP_ID
BOT_APP_ID_PIXXIE_BOT = pixxie_bot_config.BOT_APP_ID

SERVER_ID_MCFLYS_SERVER = 1069374877741617282
SERVER_ID_DTF = 1312555548100406846364

SCHEDULER_INTERVALL = 300 # 300 Sekunden = 5 Minuten