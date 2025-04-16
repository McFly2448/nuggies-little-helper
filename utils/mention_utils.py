import discord
from . import emoji
from logger_config import setup_logger
from utils.role_utils import RoleUtils
from utils.user_utils import UserUtils

class MentionUtils:
    # Logger initialisieren
    logger = setup_logger(__name__)

    @staticmethod
    def get_mention(guild: discord.Guild, id: int) -> str:
        MentionUtils.logger.debug(f"MentionsUtils sucht die Rolle / den User mit ID {id} in dem Server {guild.name}")
        role = RoleUtils.find_role_by_id(guild.roles, id)
        if role:
            return role.mention
        
        member = UserUtils.find_member(guild, id)
        if member:
            return member.mention
        
        MentionUtils.logger.error(f"{emoji.WARNING} Fehler: ID {id} ist weder eine Rolle noch ein Member!")
        return