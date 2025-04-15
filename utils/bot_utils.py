import discord
import re

class BotUtils:
    @staticmethod
    async def has_bot_a_messages_after_bot_b(channel: discord.channel, user_id_bot_a: int, user_id_bot_b: int) -> bool:
        last_message = None  # Speichert die letzte gelesene Nachricht
        limit_messages = 100
        while True:  # Solange es Nachrichten gibt
            messages = [message async for message in channel.history(limit=limit_messages, before=last_message)] if last_message else [message async for message in channel.history(limit=limit_messages)]  # Nächste 100 Nachrichten abrufen
            if not messages:  # Keine weiteren Nachrichten? -> Abbrechen
                break

            for message in messages:
                if message.author.id == user_id_bot_a:
                    # Es wurde eine Bot A Nachricht gefunden (und das bevor eine Bot B Nachricht gefunden wurde)
                    return True
                if message.author.id == user_id_bot_b:
                    # Es wurde eine Bot B Nachricht gefunden (und das bevor eine Bot A Nachricht gefunden wurde)
                    return False        
            last_message = messages[-1]  # Letzte Nachricht für den nächsten API-Call setzen
        # Es wurde weder Bot A noch B gefunden
        return False