from dotenv import load_dotenv
import os

from rumble_royale import rumble_royale_config
from pixxie_bot import pixxie_bot_config

load_dotenv()  # Lädt Variablen aus der .env-Datei
BOT_TOKEN = os.getenv("BOT_TOKEN")

BOT_APP_ID_RUMBLE_ROYALE = rumble_royale_config.BOT_APP_ID
BOT_APP_ID_PIXXIE_BOT = pixxie_bot_config.BOT_APP_ID