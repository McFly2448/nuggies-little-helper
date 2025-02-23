import discord
import re
from . import rumble_royale_config
from utils import emoji
from utils.role_utils import RoleUtils
from utils.user_utils import UserUtils

class RumbleRoyaleHandler:
    async def handle_message(self, message: discord.Message):
        if message.author.id != rumble_royale_config.BOT_APP_ID:
            return  # Ignorieren, wenn es nicht der gesuchte Benutzer ist
        
        """Verarbeitet Nachrichten vom Rumble Royale Bot"""
        if message.embeds:
            for embed in message.embeds:
                # Reagiere auf ein Kampf Start
                await self.on_command_battle(message, embed)
                
                # Reagiere auf einen Gewinner
                await self.on_event_winner(message, embed)
                
    #
    # Rumble Royale Bot - Kampf Start Nachricht
    #
    async def on_command_battle(self, message: discord.Message, embed: discord.Embed):
        if embed.title and embed.title.startswith(rumble_royale_config.EMBED_TITLE_HOSTED_BY):
            role_ping = RoleUtils.find_role_by_guild(rumble_royale_config.ROLE_NEW_BATTLE_PING_IDS, message.guild)
            if not role_ping:
                print(f'Rumble Royale Role Ping nicht gefunden')
                return
            await message.channel.send(f'{role_ping.mention} - a new rumble royale battle has been initiated!')

    #
    # Rumble Royale Bot - Sieger Nachricht
    #
    async def on_event_winner(self, message: discord.Message, embed: discord.Embed):
        if embed.title and rumble_royale_config.EMBED_TITLE_WINNER in embed.title:                     
            mentions = UserUtils.find_user_in_text(message)
            if mentions:
                mention_text = " ".join(f"{RoleUtils.get_user_greeting(user, message.guild)}" for user in mentions)
                await message.channel.send(f'congratulation {mention_text} {emoji.EMOJI_EEVEE_CLAP}{emoji.EMOJI_EEVEE_CLAP}{emoji.EMOJI_EEVEE_CLAP}')