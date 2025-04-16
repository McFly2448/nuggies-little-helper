import discord
from discord.ext import commands
from . import coordle_config
from logger_config import setup_logger
from utils import emoji
from utils.bot_utils import BotUtils

class CoordleHandler:
    # Logger initialisieren
    logger = setup_logger(__name__)

    def __init__(self, bot: commands.Bot):
        self.bot = bot  # Speichert den Bot

    async def handle_message(self, messageOld: discord.Message, messageNew: discord.Message):
        if messageNew.author.id != coordle_config.BOT_APP_ID:
            self.logger.debug(f"Die Nachricht <{messageNew.content}> hat den falschen Author {messageNew.author.name}")
            return  # Ignorieren, wenn es nicht der gesuchte Benutzer ist
        
        if await BotUtils.has_bot_a_messages_after_bot_b(messageNew.channel, self.bot.user.id, coordle_config.BOT_APP_ID):
            self.logger.debug(f"Dieser Bot mit ID {self.bot.user.id} hat im Kanal {messageNew.channel.name} nach dem Coordle Bot eine Nachricht geschrieben, von daher ist keine Verarbeitung notwendig")
            return  # Ignorieren, wenn der eigene Bot bereits Nachrichten NACH der letzten Coordle Bot Nachricht geschrieben hatte

        if not messageOld:
            self.logger.debug(f"Verarbeite im Kanal {messageNew.channel.name} die neue Message <{messageNew.content}>")
        else:
            self.logger.debug(f"Verarbeite im Kanal {messageNew.channel.name} die Editierung der alten Message <{messageOld.content}> zur neuen Message <{messageNew.content}>")
        
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