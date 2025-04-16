import discord
import re
from logger_config import setup_logger

class UserUtils:
    # Logger initialisieren
    logger = setup_logger(__name__)

    @staticmethod
    def find_user_in_text(message: discord.Message) -> list[discord.User | discord.Member]:
        UserUtils.logger.debug(f"UserUtils sucht in der Message <{message.content}> nach Mentions")
        # return re.findall(r"<@!?(\d+)>", message.content)
        return message.mentions
    
    @staticmethod
    def find_member(guild: discord.Guild, member_id: int) -> discord.Member:
        UserUtils.logger.debug(f"UserUtils sucht im Server {guild.name} nach den User mit ID {member_id}")
        return guild.get_member(member_id)