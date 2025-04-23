import discord
import random
from typing import Sequence, Optional
from . import utils_config
from logger_config import setup_logger

class RoleUtils:
    # Logger initialisieren
    logger = setup_logger(__name__)

    @staticmethod
    def find_role_by_id(roles: Sequence[discord.Role], role_id: int) -> Optional[discord.Role]:
        RoleUtils.logger.debug(f"RoleUtils sucht die Rolle mit ID {role_id} innerhalb der übergebenen Sequence")
        return discord.utils.get(roles, id=role_id)
    
    @staticmethod
    def find_role_by_guild(role_ids: dict[int, int], guild: discord.Guild) -> Optional[discord.Role]:
        RoleUtils.logger.debug(f"RoleUtils sucht für den Server {guild.name} nach einer Rolle innerhalb von dem übergebenem dict")
        if guild.id in role_ids:
            role_id = role_ids[guild.id]
            if not role_id:
                RoleUtils.logger.error(f'Rolle nicht gefunden')
            return guild.get_role(role_id)
    
    @staticmethod
    def get_user_greeting(user: discord.User, guild: discord.Guild) -> str:
        RoleUtils.logger.debug(f"RoleUtils sucht für den User {user.name} vom Server {guild.name} nach einer passenden Anrede")
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
            RoleUtils.logger.warning(f'Keine Anrede ermittelt')
            return f"{user.mention}"

        return f"{title} {user.mention}"