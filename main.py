import discord
import config
from keep_alive import keep_alive
from utils import emoji
from rumble_royale.rumble_royale_handler import RumbleRoyaleHandler
from pixxie_bot.pixxie_bot_handler import PixxieBotHandler

class MyClient(discord.Client):
    def __init__(self, *, intents):
        super().__init__(intents=intents)
        self.rumble_royale_handler = RumbleRoyaleHandler()
        self.pixxie_bot_handler = PixxieBotHandler()

    async def on_ready(self):
        print(f'{emoji.EMOJI_CHECKMARK_GREEN} Bot ist eingeloggt als {self.user}')

    async def on_message(self, message):
        """Wird aufgerufen, wenn eine neue Nachricht gesendet wird."""
        if message.author.bot:  # Reagiere nur auf bestimmte Bots
            if message.author.id == config.BOT_APP_ID_RUMBLE_ROYALE:
                await self.rumble_royale_handler.handle_message(message)
            elif message.author.id == config.BOT_APP_ID_PIXXIE_BOT:
                await self.pixxie_bot_handler.handle_message(message)

    async def on_message_edit(self, before, after):
        """Wird aufgerufen, wenn eine Nachricht bearbeitet wird."""
        if after.author.bot: # Reagiere nur auf bestimmte Bots
            if after.author.id == config.BOT_APP_ID_RUMBLE_ROYALE:
                await self.rumble_royale_handler.handle_message(after)
            elif after.author.id == config.BOT_APP_ID_PIXXIE_BOT:
                await self.pixxie_bot_handler.handle_message(after)

# Intents aktivieren
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True

client = MyClient(intents=intents)

# Startet den Webserver
keep_alive()

# Bot starten
client.run(config.BOT_TOKEN)