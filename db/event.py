import random

import discord
from discord import Color, ChannelType
from peewee import *

from bot import api
from db.views import Views
from db.guilds import Guilds
from ui.eventDeleteModal import EventDeleteModal
from ui.eventEmbed import EventEmbed
from ui.eventModal import EventModal
from ui.eventView import EventView
from ui.viewType import ViewType

db = SqliteDatabase('db/data/events.db')


class Event(Model):
    id = IntegerField()
    name = CharField()
    description = CharField(null=True)
    when = CharField(null=True)
    where = CharField(null=True)
    date = DateField()
    channel = IntegerField()
    message = IntegerField()
    going = CharField(null=True)
    notGoing = CharField(null=True)
    otherAttendees = CharField(null=True)
    announced = BitField()
    announced_message = IntegerField()
    thread = IntegerField()
    createdBy = CharField()
    color = IntegerField()

    class Meta:
        database = db

    async def build(self, interaction: discord.Interaction):
        query = Guilds.get_by_id(interaction.guild.id).channel
        channel = api.bot.get_channel(query)
        message = await api.message(channel, "@everyone")
        view = Views.create(guild=interaction.guild.id, type=ViewType.EVENT.value, channel=channel.id, message=message.id)
        r = lambda: random.randint(0, 255)
        self.id = view.id
        self.channel = channel.id
        self.message = message.id
        self.announced = 0
        self.going = interaction.user.id
        self.createdBy = interaction.user
        self.color = Color.from_rgb(r(), r(), r())
        thread = await message.create_thread(name=self.name)
        await thread.send(content="This thread will self-destruct the day after the event.")
        self.announced_message = thread.id
        self.event = Event.create(id=self.id, name=self.name, description=self.description, when=self.when,
                                  where=self.where, date=self.date, channel=self.channel, message=self.message,
                                  going=self.going, notGoing=self.notGoing, otherAttendees=self.otherAttendees,
                                  announced=self.announced, createdBy=self.createdBy, announced_message=self.announced_message, thread=self.announced_message,
                                  color=Color.from_rgb(r(), r(), r()))
        self.eventMessage = message
        return await self.refresh(interaction)

    async def refresh(self, interaction = None, create=False):
        try:
            self.save()
            attendees = await self.getAttendees()
            view = EventView(self)

            if interaction is None:
                if create:
                    channel = api.bot.get_channel(self.channel)
                    self.eventMessage = await api.message(channel, "@everyone")
                    self.message = self.eventMessage.id
                    thread = await self.eventMessage.create_thread(name=self.name)
                    await thread.send(content="This thread will self-destruct the day after the event.")
                    self.announced_message = thread.id
                    self.save()
                    v = Views.get_by_id(self.id)
                    v.message = self.eventMessage.id
                    v.save()

            await self.eventMessage.edit(content="", view=view, embed=EventEmbed(self, attendees))
            if interaction:
                await interaction.response.defer()

        except Exception as e:
            print(f"Error refreshing event {e}")

    async def edit(self, interaction):
        try:
            await interaction.response.send_modal(EventModal(self, update=True))
        except Exception as e:
            print(f"Error editing event {e}")

    async def getAttendees(self):
        g = []
        if self.going and self.going != "None":
            for id in str(self.going).split(","):
                user = await api.bot.fetch_user(id)
                print(user)
                g.append(user.name)
            return str.join(", ", g)
        return None

    async def announce(self):
        if not self.announced:
            if self.going:
                print(f"announced {self.name}!")
                going = str(self.going).split(",")
                mentions = []
                for g in going:
                    print(g)
                    user = await api.bot.get_or_fetch_user(g)
                    print(user)
                    mentions.append(user.mention)
                thread = api.bot.get_channel(self.announced_message)
                await thread.send(content=f"Hey {', '.join(mentions)}, this event is happening today!")
                self.announced = True
                self.save()

    async def deleteEvent(self, interaction):
        try:
            await interaction.response.send_modal(EventDeleteModal(self))
        except Exception as e:
            print(f"Error deleting event {e}")

    async def remove(self):
        print(f"Removing '{self.name}'")
        message = await api.bot.get_channel(self.channel).fetch_message(self.message)
        thread = api.bot.get_channel(self.announced_message)
        try:
            self.delete_instance()
        except Exception as e:
            print(f"Error 4 {e}")
        try:
            Views.get_by_id(self.id).delete_instance()
        except Exception as e:
            print(f"Error 5 {e}")
        await message.delete()
        await thread.delete()


def initialize_db():
    db.connect()
    db.create_tables([Event], safe=True)
    db.close()


initialize_db()
