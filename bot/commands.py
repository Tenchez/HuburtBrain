import discord
from discord.ext import commands

from db.event import Event
from ui.eventModal import EventModal
from ui.updateView import UpdateView


class Commands(commands.Cog):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_

    @commands.slash_command(name="create")
    async def create(self, ctx: discord.ApplicationContext):
        await ctx.interaction.response.send_modal(EventModal(Event()))

    @commands.slash_command(name="update", description="Friendly Event update")
    async def update(self, ctx: discord.ApplicationContext):
        await UpdateView().send(ctx)
