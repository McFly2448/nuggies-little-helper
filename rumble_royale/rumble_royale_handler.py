import discord
from discord.ext import commands
from collections import deque
from . import rumble_royale_config
from logger_config import setup_logger
from utils import emoji
from utils.bot_utils import BotUtils
from utils.role_utils import RoleUtils
from utils.user_utils import UserUtils

class RumbleRoyaleHandler:
    # Logger initialisieren
    logger = setup_logger(__name__)

    # Nur IDs, auf die der Bot wirklich reagiert hat; merkt sich nur die letzten 500 IDs
    already_reacted_ids = deque(maxlen=500)

    def __init__(self, bot: commands.Bot):
        self.bot = bot  # Speichert den Bot
        
    async def handle_message(self, messageOld: discord.Message, messageNew: discord.Message):
        if messageNew.author.id != rumble_royale_config.BOT_APP_ID:
            self.logger.debug(f"Die Nachricht <{messageNew.content}> hat den falschen Author {messageNew.author.name}")
            return  # Ignorieren, wenn es nicht der gesuchte Benutzer ist
        
        if await BotUtils.has_bot_a_messages_after_bot_b(messageNew.channel, self.bot.user.id, rumble_royale_config.BOT_APP_ID):
            self.logger.debug(f"Dieser Bot mit ID {self.bot.user.id} hat im Kanal {messageNew.channel.name} nach dem Rumble Royale Bot eine Nachricht geschrieben, von daher ist keine Verarbeitung notwendig")
            return  # Ignorieren, wenn der eigene Bot bereits Nachrichten NACH der letzten Rumble Royale Bot Message geschrieben hatte

        if not messageOld:
            self.logger.debug(f"Verarbeite im Kanal {messageNew.channel.name} die neue Message <{messageNew.content}>")
        else:
            self.logger.debug(f"Verarbeite im Kanal {messageNew.channel.name} die Editierung der alten Message <{messageOld.content}> zur neuen Message <{messageNew.content}>")
        
        """Verarbeitet Nachrichten vom Rumble Royale Bot"""
        if messageNew.embeds:
            for embed in messageNew.embeds:
                # Reagiere auf ein Kampf Start
                await self.on_command_battle(messageNew, embed)
                
                # Reagiere auf einen Gewinner
                await self.on_event_winner(messageNew, embed)

    #
    # Rumble Royale Bot - Kampf Start Nachricht
    #
    async def on_command_battle(self, message: discord.Message, embed: discord.Embed):
        self.logger.debug(f"Es wird im Kanal {message.channel.name} geprüft, ob die Message <{message.content}> mit dem Embed Titel <{embed.title}> ein neues rumble royale battle initiiert wurde")
        if embed.title and embed.title.startswith(rumble_royale_config.EMBED_TITLE_HOSTED_BY):
            role_ping = RoleUtils.find_role_by_guild(rumble_royale_config.ROLE_NEW_BATTLE_PING_IDS, message.guild)
            if not role_ping:
                self.logger.error(f'Rumble Royale Role Ping nicht gefunden')
                return
            if(message.id in self.already_reacted_ids):
                self.logger.debug(f"Dieser Bot mit ID {self.bot.user.id} hat im Kanal {message.channel.name} auf die Nachricht mit {message.id} bereits reagiert, von daher ist keine weitere Verarbeitung notwendig")
                return # Wenn auf die Nachricht bereits reagiert wurde, dann ist ein erneutes reagieren falsch, darum gehen wir dann raus
            self.already_reacted_ids.append(message.id)
            await message.channel.send(f'{role_ping.mention} - a new rumble royale battle has been initiated!')

    #
    # Rumble Royale Bot - Sieger Nachricht
    #
    async def on_event_winner(self, message: discord.Message, embed: discord.Embed):
        self.logger.debug(f"Es wird im Kanal {message.channel.name} geprüft, ob die Message <{message.content}> mit dem Embed Titel <{embed.title}> eine Sieger Nachricht ist")
        if embed.title and rumble_royale_config.EMBED_TITLE_WINNER in embed.title:
            mentions = UserUtils.find_user_in_text(message)
            if mentions:
                mention_text = " ".join(f"{RoleUtils.get_user_greeting(user, message.guild)}" for user in mentions)
                if(message.id in self.already_reacted_ids):
                    self.logger.debug(f"Dieser Bot mit ID {self.bot.user.id} hat im Kanal {message.channel.name} auf die Nachricht mit {message.id} bereits reagiert, von daher ist keine weitere Verarbeitung notwendig")
                    return # Wenn auf die Nachricht bereits reagiert wurde, dann ist ein erneutes reagieren falsch, darum gehen wir dann raus
                self.already_reacted_ids.append(message.id)
                await message.channel.send(f'congratulations {mention_text} {emoji.CLAP_EEVEE}{emoji.CLAP_EEVEE}{emoji.CLAP_EEVEE}')
                await self.send_reminder_for_battle(message.channel)

    #
    # Rumble Royale Bot - Erinnerung an den /battle bzw. /start Initator senden
    #
    async def send_reminder_for_battle(self, channel: discord.TextChannel):
        self.logger.debug(f"Es wird im Kanal {channel.name} geprüft, ob ein Reminder notwendig ist")
        # Nachrichtenverlauf durchsuchen (letzte 100 Nachrichten)
        async for msg in channel.history(limit=100, oldest_first=False):
            if msg.author.id == rumble_royale_config.BOT_APP_ID and msg.embeds and msg.interaction_metadata:
                for embed in msg.embeds:
                    if embed.title and embed.title.startswith(rumble_royale_config.EMBED_TITLE_HOSTED_BY):
                        command_user = msg.interaction_metadata.user
                        if command_user:
                            self.logger.debug(f"Im Kanal {channel.name} ist ein Reminder notwendig")
                            await channel.send(f"Hey {command_user.mention}, don't forget to start the next battle with `/battle`!")
                            return  # Stoppe, sobald der erste Treffer gefunden wurde