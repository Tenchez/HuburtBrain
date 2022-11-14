import discord
from discord.ext import commands

from bot import api, time
from db.event import Event
from db.guilds import Guilds
from db.views import Views
from ui.eventManagerView import EventManagerView
from ui.viewType import ViewType


class Events(commands.Cog):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have logged in as {self.bot.user}')

        guilds = self.bot.guilds
        for guild in guilds:
            print(guild.id)

            channel = await api.setupChannel(guild)
            createMessage = await api.setupCreateEvent(guild,channel)
            await api.setupEvents(guild,channel)

        while True:
            await time.checkTime()


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"Joined guild {guild}")
        # try:
        #     channel = Views.select(Views.channel).where(Views.guild == guild).get()
        # except Exception as e:
        #     print("No event channel... creating...")
        #     channel = await guild.create_text_channel("📅Upcoming-Events")
        #     try:
        #         Guilds.create(guild=guild.id, channel=channel.id)
        #         await channel.set_permissions(guild.default_role, send_messages=False)
        #     except Exception as e:
        #         print(f"Error 9 {e}")
        # finally:
        #     print(f"Found channel")
        # try:
        #     message = await EventManagerView.build(channel=channel)
        #     view = Views.create(guild=guild.id, type=ViewType.CREATE_NEW_EVENT.value, channel=channel.id,
        #                         message=message.id)
        # except Exception as e:
        #     print(f"Error 8 {e}")


def setup(bot):
    bot.add_cog(Events(bot))
