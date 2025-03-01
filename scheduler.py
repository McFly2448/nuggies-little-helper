import discord
from discord.ext import commands
import asyncio
import config
from utils import emoji
from pixxie_bot.pixxie_bot_handler import PixxieBotHandler

class Scheduler:
    def __init__(self, bot: commands.bot):
        super().__init__()
        self.bot = bot
        self.pixxie_bot_handler = PixxieBotHandler(bot)

    async def start(self):
        await self.bot.wait_until_ready() # Sicherstellen, dass der Bot bereit ist
        while not self.bot.is_closed():
            try:
                await self.check_hangry_games()
            except Exception as e:
                print(f"{emoji.WARNING} Fehler: {e}")
            await asyncio.sleep(config.SCHEDULER_INTERVALL)
    
    async def check_hangry_games(self):
        await self.pixxie_bot_handler.send_reminder_for_hangry_games()