import discord
from . import pixxie_bot_config
from utils import emoji
from utils.role_utils import RoleUtils
from utils.user_utils import UserUtils

class PixxieBotHandler:
    async def handle_message(self, messageOld: discord.Message, messageNew: discord.Message):
        if messageNew.author.id != pixxie_bot_config.BOT_APP_ID:
            return  # Ignorieren, wenn es nicht der gesuchte Benutzer ist
        
        """Verarbeitet Nachrichten vom Hangry Games Bot"""
        if messageNew.embeds:
            for embed in messageNew.embeds:
                # Reagiere auf ein Hangry Games Start
                await self.on_command_hangrygames_new(messageOld, messageNew, embed)
                
                # Reagiere auf einen Gewinner
                await self.on_event_winner(messageNew, embed)
    
    #
    # Pixxie Bot - Hangry Games - Start Nachricht
    #
    async def on_command_hangrygames_new(self, messageOld: discord.Message, messageNew: discord.Message, embed: discord.Embed):
        # Es darf nur bei der Neuanlage der Nachricht (messageOld == None) reagieren. 
        # Ist die messageOld vorhanden, dann ist es keine Neuanlage und man verlässt die Methode
        # Und es braucht einen embed mit title und description
        if messageOld or not embed or not embed.title or not embed.description:
            return
        
        # Überprüfen, ob der Titel dem gewünschten Muster entspricht
        title_match = pixxie_bot_config.EMBED_TITLE_PATTERN_NEW_HANGRY_GAMES.match(embed.title)
        
        # Überprüfen, ob die erste Zeile der Beschreibung dem erwarteten Text entspricht
        first_line = embed.description.split("\n")[0] if embed.description else ""

        if title_match and first_line == pixxie_bot_config.EMBED_DESCRIPTION_SETTING_THE_TABLE:
            role_ping = RoleUtils.find_role_by_guild(pixxie_bot_config.ROLE_HANGRY_GAMES_PING_IDS, messageNew.guild)
            if not role_ping:
                print(f'Hangry Games Role Ping nicht gefunden')
                return
            await messageNew.channel.send(f'{role_ping.mention} - a new hangry games has been initiated!')
    
    #
    # Pixxie Bot - Hangry Games - Sieger Nachricht
    #
    async def on_event_winner(self, message: discord.Message, embed: discord.Embed):
        if embed.title and pixxie_bot_config.EMBED_TITLE_WINNER in embed.title:                     
            mentions = UserUtils.find_user_in_text(message)
            if mentions:
                mention_text = " ".join(f"{RoleUtils.get_user_greeting(user, message.guild)}" for user in mentions)
                await message.channel.send(f'congratulations {mention_text} {emoji.CLAP_EEVEE}{emoji.CLAP_EEVEE}{emoji.CLAP_EEVEE}')