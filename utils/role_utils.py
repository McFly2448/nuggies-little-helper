import discord
from typing import Sequence, Optional

class RoleUtils:
    @staticmethod
    def find_role_by_id(roles: Sequence[discord.Role], role_id: int) -> Optional[discord.Role]:
        return discord.utils.get(roles, id=role_id)
    
    @staticmethod
    def find_role_by_guild(role_ids: dict[int, int], guild: discord.Guild) -> Optional[discord.Role]:
        if guild.id in role_ids:
            role_id = role_ids[guild.id]
            return guild.get_role(role_id)