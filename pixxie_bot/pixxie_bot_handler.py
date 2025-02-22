import discord
from pixxie_bot import pixxie_bot_config

class PixxieBotHandler:
    async def handle_message(self, message: discord.Message):
        if message.author.id != pixxie_bot_config.BOT_APP_ID:
            return  # Ignorieren, wenn es nicht der gesuchte Benutzer ist
        
        """Verarbeitet Nachrichten vom Hangry Games Bot"""
        if message.embeds:
            embed = message.embeds[0]
            if embed.title and embed.title.startswith("Hangry Games"):
                await message.channel.send(f"🍔 Hangry Games erkannt: {embed.title}")