import discord
import asyncio
import config
from utils import emoji
from pixxie_bot.pixxie_bot_handler import PixxieBotHandler

class Scheduler:
    def __init__(self, client: discord.Client):
        super().__init__()
        self.client = client
        self.pixxie_bot_handler = PixxieBotHandler(client)

    async def start(self):
        await self.client.wait_until_ready() # Sicherstellen, dass der Bot bereit ist
        while not self.client.is_closed():
            try:
                await self.check_hangry_games()
            except Exception as e:
                print(f"{emoji.WARNING} Fehler: {e}")
            await asyncio.sleep(config.SCHEDULER_INTERVALL)
    
    async def check_hangry_games(self):
        await self.pixxie_bot_handler.send_reminder_for_hangry_games()