import discord
import re

class UserUtils:
    @staticmethod
    def find_user_in_text(message: discord.Message) -> list[discord.User | discord.Member]:
        # return re.findall(r"<@!?(\d+)>", message.content)
        return message.mentions