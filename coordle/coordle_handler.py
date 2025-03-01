import discord
from discord.ext import commands
from . import coordle_config
from utils import emoji

class CoordleHandler:
    def __init__(self, bot: commands.Bot):
        self.bot = bot  # Speichert den Bot

    async def handle_message(self, messageOld: discord.Message, messageNew: discord.Message):
        if messageNew.author.id != coordle_config.BOT_APP_ID:
            return  # Ignorieren, wenn es nicht der gesuchte Benutzer ist
        
        """Verarbeitet Nachrichten vom Coordle Bot"""
        if messageNew.embeds:
            for embed in messageNew.embeds:
                # Reagiere auf ein gelöstes Spiel
                await self.on_event_game_solved(messageOld, messageNew, embed)

    #
    # Coordle Bot - Spiel gelöst Nachricht
    #
    async def on_event_game_solved(self, messageOld: discord.Message, messageNew: discord.Message, embed: discord.Embed):
        # Es darf nur bei der Neuanlage der Nachricht (messageOld == None) reagieren. 
        # Ist die messageOld vorhanden, dann ist es keine Neuanlage und man verlässt die Methode
        # Und es braucht einen embed mit fields
        if messageOld or not embed or not embed.fields:
            return
        
        for field in embed.fields:
            if coordle_config.EMBED_DESCRIPTION_SOLVED in field.value:
                await messageNew.channel.send(f'{emoji.CLAP_EEVEE}{emoji.CLAP_EEVEE}{emoji.CLAP_EEVEE}')