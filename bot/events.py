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
        allGuildsChannels = Guilds.select()
        for guild in allGuildsChannels:
            query = Views.select().where(Views.type == ViewType.CREATE_NEW_EVENT.value, Views.guild == guild.guild)
            if not query.exists():
                print("Building event manager...")
                channel = api.bot.get_channel(guild.channel)
                await channel.purge(limit=9999)
                await EventManagerView.build(channel=channel)
            else:
                createEvent = query.get()
                message = await api.bot.get_channel(guild.channel).fetch_message(createEvent.message)
                await EventManagerView.build(message=message)

        query = Views.select().where(Views.type == ViewType.EVENT.value)
        print("Events:")
        if not query.exists():
            return
        for view in query:
            try:
                event = Event.get_by_id(view.id)
                print(f"{view.id} - {event.name}")
                event.eventMessage = await api.bot.get_channel(event.channel).fetch_message(event.message)
                await event.refresh()
            except Exception as e:
                print(f"Cant find event {view.id}")
                print(f"Error 7 {e}")
                try:
                    message = await api.bot.get_channel(view.channel).fetch_message(view.message)
                    await api.deleteMessage(message)
                except Exception as e:
                    print(f"Error 1 {e}")
                try:
                    Event.get_by_id(view.id).delete_instance()
                except Exception as e:
                    print(f"Error 2 {e}")
                Views.get_by_id(view.id).delete_instance()
                print(f"Cleaned up loose entry {view.message}")
        while True:
            await time.checkTime()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"Joined guild {guild}")
        try:
            channel = Views.select(Views.channel).where(Views.guild == guild).get()
        except Exception as e:
            print("No event channel... creating...")
            channel = await guild.create_text_channel("📅Upcoming-Events")
            try:
                Guilds.create(guild=guild.id, channel=channel.id)
                await channel.set_permissions(guild.default_role, send_messages=False)
            except Exception as e:
                print(f"Error 9 {e}")

            print(f"Error 3 {e}")
        finally:
            print(f"Found channel")
        try:
            await EventManagerView.build()
            view = Views.create(guild=guild.id, type=ViewType.CREATE_NEW_EVENT.value, channel=channel.id,
                                message=message.id)
        except Exception as e:
            print(f"Error 8 {e}")


def setup(bot):
    bot.add_cog(Events(bot))
