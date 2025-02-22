import discord
from typing import Sequence, Optional

class RoleUtils:
    @staticmethod
    def find_role_by_id(roles: Sequence[discord.Role], role_id: int) -> Optional[discord.Role]:
        return discord.utils.get(roles, id=role_id)