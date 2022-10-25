import os

import discord

from bot.commands import Commands
from bot.events import Events

my_secret = os.environ['DISCORD_BOT_SECRET']
description = """
Huburt
"""
intents = discord.Intents.all()
bot = discord.Bot(intents=intents, debug_guilds=[1011970418824982548])
bot.add_cog(Commands(bot))
bot.add_cog(Events(bot))
