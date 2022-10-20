import discord
from discord.ext import commands

client = commands.Bot(command_prefix=["!h ","!H ", "!Huburt ", "!huburt "], case_insensitive=True, intents=discord.Intents.all())
client.remove_command('help')