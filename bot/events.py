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

            channel = await self.setupChannel(guild)
            createMessage = await self.setupCreateEvent(guild,channel)
            await self.setupEvents(guild,channel)

        while True:
            await time.checkTime()

    async def setupChannel(self, guild):

        query = Guilds.get_or_none(Guilds.guild == guild.id)
        if query is not None:
            channel = api.bot.get_channel(query.channel)
            if channel is None:
                query.delete_instance()
                channel = await guild.create_text_channel("📅Upcoming-Events")
                try:
                    Guilds.create(guild=guild.id, channel=channel.id)
                    await channel.set_permissions(guild.default_role, send_messages=False)
                except Exception as e:
                    print(f"Error 9 {e}")
        else:
            try:
                channel = await guild.create_text_channel("📅Upcoming-Events")
                Guilds.create(guild=guild.id, channel=channel.id)
                await channel.set_permissions(guild.default_role, send_messages=False)
            except Exception as e:
                print(f"Error 10 {e}")


        return channel


    async def setupCreateEvent(self, guild,channel):
        query = Views.select().where(Views.type == ViewType.CREATE_NEW_EVENT.value, Views.guild == guild.id)
        if query.exists():
            createEvent = query.get()
            try:
                message = await api.bot.get_channel(createEvent.channel).fetch_message(createEvent.message)
                return  await EventManagerView.build(message=message)
            except discord.NotFound as e:
                query.get().delete_instance()
        guild = Guilds.select().where(Guilds.guild == guild.id)
        await channel.purge(limit=9999)
        return await EventManagerView.build(channel=channel)

    async def setupEvents(self,guild,channel):
        query = Views.select().where(Views.type == ViewType.EVENT.value, Views.guild == guild.id)
        if not query.exists():
            return
        print("Events:")
        for view in query:
            event = Event.get_by_id(view.id)
            if event is not None:
                print(event.name)
                event.eventMessage = await channel.fetch_message(event.message)
                await event.refresh()

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
