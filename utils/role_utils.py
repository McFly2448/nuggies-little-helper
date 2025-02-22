import discord
import random
from typing import Sequence, Optional
from . import utils_config

class RoleUtils:
    @staticmethod
    def find_role_by_id(roles: Sequence[discord.Role], role_id: int) -> Optional[discord.Role]:
        return discord.utils.get(roles, id=role_id)
    
    @staticmethod
    def find_role_by_guild(role_ids: dict[int, int], guild: discord.Guild) -> Optional[discord.Role]:
        if guild.id in role_ids:
            role_id = role_ids[guild.id]
            if not role_id:
                print(f'Rolle nicht gefunden')
            return guild.get_role(role_id)
    
    @staticmethod
    def get_user_greeting(user: discord.user, guild: discord.Guild) -> str:
        """Überprüft, ob ein Member die Rolle MALE oder FEMALE hat, wählt eine zufällige Anrede und gibt einen String zurück."""
        # Hole die Rollen des Users
        user_roles = {role.id for role in user.roles}

        # Prüfe auf FEMALE- oder MALE-Rolle
        role_female = RoleUtils.find_role_by_guild(utils_config.ROLE_FEMALE_IDS, guild)
        role_male = RoleUtils.find_role_by_guild(utils_config.ROLE_MALE_IDS, guild)
        if role_female and role_female.id in user_roles:
            title = random.choice(utils_config.TITLES_FEMALE)
        elif role_male and role_male.id in user_roles:
            title = random.choice(utils_config.TITLES_MALE)
        else:
            print(f'Keine Anrede ermittelt')
            return f"{user.mention}"

        return f"{title} {user.mention}"