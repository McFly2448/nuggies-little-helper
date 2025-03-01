import discord
import re
from . import coordle_config
from utils import emoji
from utils.role_utils import RoleUtils
from utils.user_utils import UserUtils

class CoordleHandler:
    async def handle_message(self, message: discord.Message):
        if message.author.id != coordle_config.BOT_APP_ID:
            return  # Ignorieren, wenn es nicht der gesuchte Benutzer ist
        
        """Verarbeitet Nachrichten vom Coordle Bot"""
        if message.embeds:
            for embed in message.embeds:
                # Reagiere auf ein gelöstes Spiel
                await self.on_event_game_solved(message, embed)

    #
    # Coordle Bot - Spiel gelöst Nachricht
    #
    async def on_event_game_solved(self, message: discord.Message, embed: discord.Embed):
        for field in embed.fields:
            if coordle_config.EMBED_DESCRIPTION_SOLVED in field.value:
                await message.channel.send(f'{emoji.CLAP_EEVEE}{emoji.CLAP_EEVEE}{emoji.CLAP_EEVEE}')