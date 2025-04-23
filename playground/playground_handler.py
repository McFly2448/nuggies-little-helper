import discord
from discord.ext import commands
from logger_config import setup_logger
from utils import emoji

class PlaygroundHandler:
    # Logger initialisieren
    logger = setup_logger(__name__)

    def __init__(self, bot: commands.Bot):
        self.bot = bot  # Speichert den Bot
        
    async def handle_message(self, messageOld: discord.Message, messageNew: discord.Message):
        if messageNew.author.id == self.bot.user.id:
            self.logger.debug(f"Die Nachricht <{messageNew.content}> stammt von diesem Bot selber")
            return  # Ignorieren, wenn es der eigene Benutzer ist
        
        if not messageOld:
            self.logger.debug(f"Verarbeite im Kanal {messageNew.channel.name} die neue Message <{messageNew.content}> vom User <{messageNew.author.name}>")
        else:
            self.logger.debug(f"Verarbeite im Kanal {messageNew.channel.name} die Editierung der alten Message <{messageOld.content}> zur neuen Message <{messageNew.content}> vom User <{messageNew.author.name}>")
        
        """Verarbeitet Nachrichten"""
        await self.handle_message_experiment_1(messageNew)

    #
    # Das erste Experiment - Attachments verarbeiten und DMs schreiben
    #
    async def handle_message_experiment_1(self, messageNew: discord.Message):
        # if messageNew.channel.id != 1364541375143608330:  
        if messageNew.channel.id != 1255848871649607730 and messageNew.channel.id != 1255591023028080641:   # nicht lokal
            self.logger.debug(f"Die Nachricht <{messageNew.content}> ist im falschen Kanal")
            return  # Falscher Kanal, also Verarbeitung abbrechen
        
        #role_id = 1083191361924251689   # nur lokal
        role_id = 1255640113052909579   # nicht lokal
        if not any(role.id == role_id for role in messageNew.author.roles):
            self.logger.debug(f"Der Author <{messageNew.author.name}> hat die falsche Rolle")
            return  # Author hat die falsche Rolle, also Verarbeitung abbrechen
        
        test_user = await self.bot.fetch_user(1085195733646446673)
        self.logger.debug(f"Der Test-User <{test_user.name}> konnte ermittelt werden")
        self.logger.debug(f"Die Nachricht <{messageNew.content}> vom User <{messageNew.author.name}> aus dem Kanal <{messageNew.channel.name}> wird verarbeitet")
        await test_user.send(content=f'Weitergeleitete Nachricht vom User <{messageNew.author.name}> aus dem Kanal <{messageNew.channel.name}>. Die Nachricht ist <{messageNew.content}>')

        if messageNew.attachments:
            MAX_ATTACHMENT_SIZE = 8 * 1024 * 1024  # 8 MB
            for attachment in messageNew.attachments:
                if attachment.size <= MAX_ATTACHMENT_SIZE:
                    file = await attachment.to_file()
                    self.logger.debug(f"Die Nachricht <{messageNew.content}> vom User <{messageNew.author.name}> aus dem Kanal <{messageNew.channel.name}> hat ein Attachment, das klein genug ist")
                    await test_user.send(content=f'Weitergeleitetes Attachment vom User <{messageNew.author.name}> aus dem Kanal <{messageNew.channel.name}>. Die Nachricht ist <{messageNew.content}>', file=file if file else None)
                else:
                    self.logger.debug(f"Die Nachricht <{messageNew.content}> vom User <{messageNew.author.name}> aus dem Kanal <{messageNew.channel.name}> hat ein Attachment, das zu groß ist")
                    await test_user.send(f"{emoji.WARNING} Attachment von <{messageNew.author.name}> aus dem Kanal <{messageNew.channel.name}> ist zu groß, hier der Link:\n{attachment.url}.")