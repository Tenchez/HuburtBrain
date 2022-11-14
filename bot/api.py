import discord

from bot.constants import bot, my_secret
from db.event import Event
from db.guilds import Guilds
from db.views import Views
from ui.eventManagerView import EventManagerView
from ui.viewType import ViewType


def startBot():
    try:
        bot.run(my_secret)
    except Exception as e:
        print(f"Error 6 {e}")


async def message(ctx, msg, view=None):
    try:
        return await ctx.send(msg, view=view)
    except Exception as e:
        print("Cannot send message: {}".format(e))


async def sendView(interaction, msg, view, hidden):
    try:
        return await interaction.response.send_message(view=view,
                                                       ephemeral=hidden)
    except Exception as e:
        print("Cannot send view: {}".format(e))


async def respond(interaction, msg, hidden):
    try:
        return await interaction.response.send_message(msg, ephemeral=hidden)
    except Exception as e:
        print("Cannot send response: {}".format(e))


async def deleteMessage(msg):
    try:
        return await msg.delete()
    except Exception as e:
        print("Cannot delete message: {}".format(e))

async def setupChannel( guild):

    query = Guilds.get_or_none(Guilds.guild == guild.id)
    channel = None
    if query is not None:
        channel = bot.get_channel(query.channel)
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


async def setupCreateEvent(guild,channel):
    query = Views.select().where(Views.type == ViewType.CREATE_NEW_EVENT.value, Views.guild == guild.id)
    if query.exists():
        createEvent = query.get()
        try:
            message = await bot.get_channel(createEvent.channel).fetch_message(createEvent.message)
            return  await EventManagerView.build(message=message)
        except discord.NotFound as e:
            query.get().delete_instance()
    guild = Guilds.select().where(Guilds.guild == guild.id)
    await channel.purge(limit=9999)
    return await EventManagerView.build(channel=channel)

async def setupEvents(guild,channel):
    query = Views.select().where(Views.type == ViewType.EVENT.value, Views.guild == guild.id)
    if not query.exists():
        return
    print("Events:")
    for view in query:
        event = Event.get_by_id(view.id)
        if event is not None:
            print(event.name)
            create=False
            try:
                event.eventMessage = await channel.fetch_message(event.message)
            except discord.NotFound:
                print(f"Message not found for {event.id}")
                create=True
            await event.refresh(create=create)