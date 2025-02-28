import discord
from . import emoji
from utils.role_utils import RoleUtils
from utils.user_utils import UserUtils

class MentionUtils:
    @staticmethod
    def get_mention(guild: discord.Guild, id: int) -> str:
        role = RoleUtils.find_role_by_id(guild.roles, id)
        if role:
            return role.mention
        
        member = UserUtils.find_member(guild, id)
        if member:
            return member.mention
        
        print(f"{emoji.WARNING} Fehler: ID {id} ist weder eine Rolle noch ein Member!")
        return