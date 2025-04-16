import discord
import re
from logger_config import setup_logger

class BotUtils:
    # Logger initialisieren
    logger = setup_logger(__name__)

    @staticmethod
    async def has_bot_a_messages_after_bot_b(channel: discord.TextChannel, user_id_bot_a: int, user_id_bot_b: int) -> bool:
        BotUtils.logger.debug(f"BotUtils verprobt, ob im Kanal {channel.name} der User A mit ID {user_id_bot_a} bereits eine Nachricht NACH User B mit ID {user_id_bot_b} geschrieben hat")
        last_message = None  # Speichert die letzte gelesene Nachricht
        limit_messages = 100
        while True:  # Solange es Nachrichten gibt
            messages = [message async for message in channel.history(limit=limit_messages, before=last_message)] if last_message else [message async for message in channel.history(limit=limit_messages)]  # Nächste 100 Nachrichten abrufen
            if not messages:  # Keine weiteren Nachrichten? -> Abbrechen
                break

            for message in messages:
                if message.author.id == user_id_bot_a:
                    # Es wurde eine Bot A Nachricht gefunden (und das bevor eine Bot B Nachricht gefunden wurde)
                    BotUtils.logger.debug(f"Der User A mit ID {user_id_bot_a} wurde zuerst gefunden")
                    return True
                if message.author.id == user_id_bot_b:
                    # Es wurde eine Bot B Nachricht gefunden (und das bevor eine Bot A Nachricht gefunden wurde)
                    BotUtils.logger.debug(f"Der User B mit ID {user_id_bot_b} wurde zuerst gefunden")
                    return False        
            last_message = messages[-1]  # Letzte Nachricht für den nächsten API-Call setzen
        # Es wurde weder Bot A noch B gefunden
        BotUtils.logger.warning(f"Im Kanal {channel.name} wurde weder eine Nachricht von User A mit ID {user_id_bot_a} noch eine Nachricht von User B mit ID {user_id_bot_b} gefunden")
        return False