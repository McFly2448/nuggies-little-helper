import os

# Installiert alle fehlenden Pakete aus requirements.txt
os.system("pip install -r requirements.txt")

import discord
from discord.ext import commands
import config
import version
from keep_alive import keep_alive
from scheduler import Scheduler
from utils import emoji
from logger_config import setup_logger
from playground.playground_handler import PlaygroundHandler
from rumble_royale.rumble_royale_handler import RumbleRoyaleHandler
from pixxie_bot.pixxie_bot_handler import PixxieBotHandler
from coordle.coordle_handler import CoordleHandler

import tracemalloc
tracemalloc.start()

# Intents aktivieren
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True

# Bot-Client mit Command-Unterstützung erstellen
bot = commands.Bot(command_prefix="!", intents=intents)

# Logger initialisieren
logger = setup_logger(__name__)

# Event: Bot ist bereit
@bot.event
async def on_ready():
    logger.info(f'{emoji.CHECK_MARK} Der Bot mit Version {version.__version__} ist eingeloggt als {bot.user}')
    bot.rumble_royale_handler = RumbleRoyaleHandler(bot)
    bot.pixxie_bot_handler = PixxieBotHandler(bot)
    bot.coordle_handler = CoordleHandler(bot)
    bot.playground_handler = PlaygroundHandler(bot)
    scheduler = Scheduler(bot)
    bot.loop.create_task(scheduler.start())
    await bot.tree.sync()  # Synchronisiert die Slash-Commands
    logger.info(f'{emoji.CHECK_MARK} Slash-Commands synchronisiert')

# Slash-Command: Version abrufen
# Zeigt die aktuelle Bot-Version
@bot.tree.command(name="version", description="Shows the current bot version")
async def version_command(interaction: discord.Interaction):
    await interaction.response.send_message(f"{emoji.ROBOT}{emoji.BABY_CHICK} **Nuggie's Little Helper** runs with version `{version.__version__}`")

# Slash-Command: Ping abrufen
# Testet die Bot-Verbindung
@bot.tree.command(name="ping", description="Tests the bot connection")
async def ping_command(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f'{emoji.PING_PONG_PADDLE} Pong! Latency: `{latency}ms`')

# Event: Nachricht erhalten
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignoriere eigene Nachrichten
    if message.author.bot:
        if message.author.id == config.BOT_APP_ID_RUMBLE_ROYALE:
            await bot.rumble_royale_handler.handle_message(None, message)
        elif message.author.id == config.BOT_APP_ID_PIXXIE_BOT:
            await bot.pixxie_bot_handler.handle_message(None, message)
        elif message.author.id == config.BOT_APP_ID_COORDLE:
            await bot.coordle_handler.handle_message(None, message)
    else:
        await bot.playground_handler.handle_message(None, message)
    await bot.process_commands(message)  # Erlaubt das Verarbeiten von !-Befehlen

# Event: Nachricht bearbeitet
@bot.event
async def on_message_edit(before, after):
    if after.author == bot.user:
        return
    if after.author.bot:
        if after.author.id == config.BOT_APP_ID_RUMBLE_ROYALE:
            await bot.rumble_royale_handler.handle_message(before, after)
        elif after.author.id == config.BOT_APP_ID_PIXXIE_BOT:
            await bot.pixxie_bot_handler.handle_message(before, after)
        elif after.author.id == config.BOT_APP_ID_COORDLE:
            await bot.coordle_handler.handle_message(before, after)
    else:
        await bot.playground_handler.handle_message(before, after)

# Auf Fehler reagieren
# zum Beispiel "Diesen Befehl kenne ich nicht!"
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        #await ctx.send(f"{emoji.CROSS_MARK} I don't know this command: {ctx.message.content}")
        return # die obere Zeile ist fürs debuggen gut, aber momentan ist es nicht notwendig.

# Bot starten
bot.run(config.BOT_TOKEN)