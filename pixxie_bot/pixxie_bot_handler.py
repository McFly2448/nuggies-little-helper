import discord
from discord.ext import commands
from datetime import datetime, timezone, timedelta
from . import pixxie_bot_config
from utils import emoji
from utils.role_utils import RoleUtils
from utils.user_utils import UserUtils
from utils.mention_utils import MentionUtils

class PixxieBotHandler:
    def __init__(self, bot: commands.Bot):
        self.bot = bot  # Speichert den Bot-Client

    async def handle_message(self, messageOld: discord.Message, messageNew: discord.Message):
        if messageNew.author.id != pixxie_bot_config.BOT_APP_ID:
            return  # Ignorieren, wenn es nicht der gesuchte Benutzer ist
        
        """Verarbeitet Nachrichten vom Pixxie Bot"""
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
        
        if await self.is_hangry_games_start_embed(embed):
            role_ping = RoleUtils.find_role_by_guild(pixxie_bot_config.ROLE_HANGRY_GAMES_PING_IDS, messageNew.guild)
            if not role_ping:
                print(f'Hangry Games Role Ping nicht gefunden')
                return
            await messageNew.channel.send(f'{role_ping.mention} - a new hangry games has been initiated!')
    
    #
    # Verprobt, ob das übergeben Embed den Start eines Hangry Games darstellt
    #
    async def is_hangry_games_start_embed(self, embed: discord.Embed) -> bool:
        # Überprüfen, ob der Titel dem gewünschten Muster entspricht
        title_match = pixxie_bot_config.EMBED_TITLE_PATTERN_NEW_HANGRY_GAMES.match(embed.title or "")
        
        # Überprüfen, ob die erste Zeile der Beschreibung dem erwarteten Text entspricht
        first_line = embed.description.split("\n")[0] if embed.description else ""

        if title_match and first_line == pixxie_bot_config.EMBED_DESCRIPTION_HANGRY_GAMES_SETTING_THE_TABLE:
            return True
        return False

    #
    # Pixxie Bot - Hangry Games - Sieger Nachricht
    #
    async def on_event_winner(self, message: discord.Message, embed: discord.Embed):
        if await self.is_hangry_games_winner_embed(embed):
            mentions = UserUtils.find_user_in_text(message)
            if mentions:
                mention_text = " ".join(f"{RoleUtils.get_user_greeting(user, message.guild)}" for user in mentions)
                await message.channel.send(f'congratulations {mention_text} {emoji.CLAP_EEVEE}{emoji.CLAP_EEVEE}{emoji.CLAP_EEVEE}')

    #
    # Verprobt ob das übergebene Embed die Sieger-Nachricht darstellt
    #
    async def is_hangry_games_winner_embed(self, embed: discord.Embed) -> bool:
        if embed.title and pixxie_bot_config.EMBED_TITLE_HANGRY_GAMES_WINNER in embed.title: 
            return True
        return False

    #
    # Schickt einen Reminder, einer laufenden Hangry Games Partie beizutreten
    #
    async def send_reminder_for_hangry_games(self):
        for channel_id, mention_id in pixxie_bot_config.MENTION_HANGRY_GAMES_REMINDER_IDS.items():
            await self.send_reminder_for_hangry_games_in_channel(channel_id, mention_id)

    #
    # Schickt einen Reminder, einer laufenden Hangry Games Partie beizutreten
    #
    async def send_reminder_for_hangry_games_in_channel(self, channel_id: int, mention_id: int):
        """Liest Nachrichten, bis das Kriterium erfüllt ist oder alle Nachrichten durch sind."""
        channel = self.bot.get_channel(channel_id)
        if not channel:
            channel = await self.bot.fetch_channel(channel_id)
        if not channel:
            print(f"Fehler: Kanal {channel_id} nicht gefunden.")
            return
        
        if not mention_id:
            print(f'Mention-ID nicht gefunden')
            return
        
        mention = MentionUtils.get_mention(channel.guild, mention_id)
        if not mention:
            print(f'Mention nicht gefunden')
            return

        now = datetime.now(timezone.utc)
        cutoff_time = now - timedelta(hours=pixxie_bot_config.INTERVALL_REMINDER_HANGRY_GAMES)
        send_reminder = False
        last_message = None  # Speichert die letzte gelesene Nachricht

        limit_messages = 100
        while True:  # Solange es Nachrichten gibt
            messages = [message async for message in channel.history(limit=limit_messages, before=last_message)] if last_message else [message async for message in channel.history(limit=limit_messages)]  # Nächste 100 Nachrichten abrufen
            if not messages:  # Keine weiteren Nachrichten? -> Abbrechen
                break

            for message in messages:
                if message.author.id == self.bot.user.id and message.content.startswith("Hey ") and message.content.endswith(" don't forget to join!"):
                    # Wenn man die letzte Erinnerung findet, dann ist eine erneute Erinnerung nicht notwendig
                    return
                
                if message.author.id == pixxie_bot_config.BOT_APP_ID and message.embeds:
                    for embed in message.embeds:
                        if await self.is_hangry_games_winner_embed(embed):
                            # Wenn man die Gewinner-Nachricht findet, dann gibt es kein laufendes Hangry Games
                            return
                        if await self.is_hangry_games_cancel_embed(embed):
                            # Wenn man die Cancel-Nachricht findet, dann gibt es kein laufendes Hangry Games
                            return
                        if await self.is_hangry_games_start_embed(embed):
                            if message.created_at < cutoff_time:
                                send_reminder = True
                                break  # Wir haben, was wir brauchen -> Abbrechen
                
                if send_reminder:
                    break # Wir haben, was wir brauchen -> Abbrechen

            if send_reminder:
                break  # Äußere Schleife beenden, wenn Nachricht gefunden wurde

            last_message = messages[-1]  # Letzte Nachricht für den nächsten API-Call setzen
        if send_reminder:
            await channel.send(f"Hey {mention} don't forget to join!")

    #
    # Verprobt ob das übergebene Embed die Cancel-Nachricht darstellt
    #
    async def is_hangry_games_cancel_embed(self, embed: discord.Embed) -> bool:
        if embed.title and pixxie_bot_config.EMBED_TITLE_HANGRY_GAMES_CANCEL in embed.title: 
            return True
        return False