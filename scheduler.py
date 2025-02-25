import discord
import asyncio
import config
from datetime import datetime, timezone
from utils import emoji
from pixxie_bot.pixxie_bot_handler import PixxieBotHandler

class Scheduler:
    def __init__(self, client: discord.Client):
        super().__init__()
        self.client = client
        self.pixxie_bot_handler = PixxieBotHandler()

    async def start(self):
        await self.client.wait_until_ready() # Sicherstellen, dass der Bot bereit ist
        while not self.client.is_closed():
            try:
                await self.check_hangry_games()
                await self.check_rumble_royale()
            except Exception as e:
                print(f"{emoji.WARNING} Fehler: {e}")
            await asyncio.sleep(config.SCHEDULER_INTERVALL)
    
    async def check_hangry_games(self):
        print(f'Prüfe Hangry Games Platzhalter')
    
    async def check_rumble_royale(self):
        print(f'Prüfe Rumble Royale Platzhalter')