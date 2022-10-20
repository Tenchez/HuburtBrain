import db_utils
import discord
import discord.utils
import formats
import helper as h
import os
import replit
import datetime
import cm
import views
from modals import CreateModal
from discord_const import client
from helper import cleanUp, announceEvent
from keep_alive import keep_alive
from replit import db
from discord.ext import tasks

if "events" not in db.keys():
    db["events"] = dict()


@tasks.loop(seconds=600)
async def cleanAnnounce():
    await cleanUp()
    await announceEvent()
    print("timed task")


@client.slash_command(description="Stops the Huburt")
async def hstop(ctx):
    await h.respond(ctx, formats.DISABLED_MSG_STRING, False)
    await client.close()


@client.command()
async def clean(ctx):
    await cleanUp()
    await h.message(ctx.message.channel, "Cleaned Events")


@client.command()
async def announce(ctx):
    await announceEvent()
    await h.message(ctx.message.channel, "Announced Events")


@client.slash_command(description="Provides information on Huburt")
async def hhelp(ctx):
    await h.respond(ctx, formats.HELP_MSG_STRING, True)


@client.command()
async def help(ctx):
    await h.message(ctx.message.channel, formats.HELP_MSG_STRING)


@client.slash_command(description="Friendly Event update")
async def hupdate(ctx):
    await views.updateEvent().send(ctx)


@client.command()
async def update(ctx, name, arg1='', arg2='', arg3=''):
    print(name + ' ' + arg1 + ' ' + arg2 + ' ' + arg3)
    if arg1 != '':
        try:
            if (arg1 != '' and arg2 != '' and arg3 != ''):
                datetime.datetime.strptime(arg3, '%m/%d/%Y')
                await db_utils.updateEvent(name, arg2, arg1, arg3)
            elif (arg1 != '' and arg2 != ''):
                datetime.datetime.strptime(arg2, '%m/%d/%Y')
                await db_utils.updateEvent(name, arg1, '', arg2)
            elif (arg1 != ''):
                await db_utils.updateEvent(name, '', arg1, '')
            await h.message(ctx.message.channel, "Updated " + name)
        except Exception as e:
            print(e)
            await h.message(
                ctx.message.channel,
                "Error updating, your actual date probably was not formatted like mm/dd/yyyy"
            )


@client.slash_command(description="Friendly Event lister")
async def hevents(ctx):
    await h.respond(ctx, db_utils.getEventListStr(), True)


@client.command()
async def events(ctx):
    await h.message(ctx.message.channel, db_utils.getEventListStr())


@client.slash_command(description="Friendly Event Creator")
async def hcreate(ctx):
    await ctx.interaction.response.send_modal(CreateModal())


@client.command()
async def create(ctx, name, where, when, hardDate):
    upcomingChannel = discord.utils.get(ctx.message.channel.guild.channels,
                                        name="upcoming-events")
    await cm.createMethod(ctx.author.id, upcomingChannel, ctx.channel, name,
                          where, when, hardDate)


@client.slash_command(description="Friendly Event Deleter")
async def hdelete(ctx):
    await views.updateEvent().send(ctx)
    #await ctx.interaction.response.send_modal(DeleteModal())


@client.command()
async def delete(ctx, name):
    await cm.deleteMethod(context=ctx, name=name)


@client.event
async def on_guild_join(guild):
    general = discord.utils.find(lambda x: x.name == 'general',
                                 guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await h.message(general, formats.WELCOME_MSG_STRING.format(guild.name))


@client.event
async def on_ready():
    replit.clear()
    h.initialize()
    cleanAnnounce.start()
    print("I'm in")
    print(client.user)


@client.event
async def on_command_error(ctx, error):
    print(error)
    await h.message(ctx.message.channel, formats.BAD_COMMAND_MSG_STRING)


#update the upcoming-events tab with reaction
@client.event
async def on_raw_reaction_add(payload):
    user = client.get_user(payload.user_id)
    print(str(payload.user_id))
    #If the bot sent the reaction
    if user == client.user:
        return
    #if the reaction is on an event in upcoming-events
    event = db_utils.getEvent(payload.message_id)
    if event is not None:
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        emoji = str(payload.emoji)
        await db_utils.updateAttending(message, event, user, emoji)
    #do other things when users react


@client.event
async def on_message(message):
    huburtsHub = str(message.channel) == "huburts-hub"
    msg = message.content
    if message.author == client.user:
        return
    if (msg.startswith(("!h ", "!H ", "!Huburt ", "!huburt "))):
        if huburtsHub:
            ##Required to process commands after consuming on_message
            await client.process_commands(message)
        else:
            await h.message(message.channel, formats.SORRY_MSG_STRING)


my_secret = os.environ['DISCORD_BOT_SECRET']
keep_alive()
try:
    client.run(my_secret)
except:
    os.system("kill 1")
