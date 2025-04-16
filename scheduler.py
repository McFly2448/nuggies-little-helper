import discord
from discord.ext import commands
import asyncio
import config
from utils import emoji
from logger_config import setup_logger
from pixxie_bot.pixxie_bot_handler import PixxieBotHandler

class Scheduler:
    # Logger initialisieren
    logger = setup_logger(__name__)

    def __init__(self, bot: commands.bot):
        super().__init__()
        self.bot = bot
        self.pixxie_bot_handler = PixxieBotHandler(bot)

    async def start(self):
        await self.bot.wait_until_ready() # Sicherstellen, dass der Bot bereit ist
        self.logger.debug(f"{emoji.CHECK_MARK} Scheduler ist gestartet")
        while not self.bot.is_closed():
            self.logger.debug(f"{emoji.CHECK_MARK} Scheduler ist noch am laufen")
            try:
                await self.check_hangry_games()
            except Exception as e:
                self.logger.error(f"{emoji.WARNING} Fehler: {e}")
            await asyncio.sleep(config.SCHEDULER_INTERVALL)
    
    async def check_hangry_games(self):
        self.logger.debug(f"Scheduler für Hangry Gamges")
        await self.pixxie_bot_handler.send_reminder_for_hangry_games()