import discord
import db_utils
from event import Event
from replit import db
from discord_const import client
import datetime
from pytz import timezone


def initialize():
    discord.User.uid = uid


#Get full username from User: <name>#<num>
def uid(self):
    return self.name + "#" + self.discriminator


def uidToName(uid):
    print('uid: ' + str(str(uid).rfind('#')))
    return str(uid)[0:(int(str(uid).rfind('#')))]


###################################################
#For interacting with discord in a 'safe' manner
###################################################


async def message(ctx, msg):
    try:
        return await ctx.send(msg)
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


async def addReaction(msg, emoji):
    try:
        return await msg.add_reaction(emoji)
    except Exception as e:
        print("Cannot send reaction: {}".format(e))


async def deleteReaction(msg, user, emoji):
    return await msg.remove_reaction(emoji, user)


async def deleteMessage(msg):
    try:
        return await msg.delete()
    except Exception as e:
        print("Cannot delete message: {}".format(e))


async def restartHuburt():
    # my_secret = os.environ['DISCORD_BOT_SECRET']
    # client.run(my_secret)
    print("I need restarted")


async def cleanUp():
    tz = timezone("US/Eastern")
    current_day = datetime.datetime.now(tz)
    formatted_date = datetime.date.strftime(current_day, "%m/%d/%Y")
    date1 = datetime.datetime.strptime(formatted_date, '%m/%d/%Y')
    for event in db["events"].keys():
        date2 = datetime.datetime.strptime(db["events"][event]["hardDate"],
                                           '%m/%d/%Y')
        if (date2 < date1):
            print("deleting event " + str(date2))
            eventObj = db_utils.deleteEvent(event)
            await cleanUpMessages(eventObj)


async def cleanUpMessages(event):
    try:
        print(event)
        print(Event.toString(event))
        message = await client.get_channel(int(event.channel)
                                           ).fetch_message(int(event.id))
        await deleteMessage(message)
        if event.announced != False:
            announce = await client.get_channel(int(
                event.channel)).fetch_message(int(event.announced))
            await deleteMessage(announce)
    except Exception as e:
        print(e)
        print('not found')


async def announceEvent():
    print("here")
    tz = timezone("US/Eastern")
    current_day = datetime.datetime.now(tz)
    formatted_date = datetime.date.strftime(current_day, "%m/%d/%Y")
    date1 = datetime.datetime.strptime(formatted_date, '%m/%d/%Y')
    print("here2")
    for event in db["events"].keys():
        print("here3")
        date2 = datetime.datetime.strptime(db["events"][event]["hardDate"],
                                           '%m/%d/%Y')
        print("date1:" + str(date1) + " date2:" + str(date2))
        print("announced id: " + str(db["events"][event]["announced"]))
        if (date2 == date1 and db["events"][event]["announced"] == False):
            print(db["events"][event]["attendees"])
            msg = ', '.join(
                map('<@{0}>'.format, db['events'][event]["attendees"].keys())
            ) + '\n\n**{}**'.format(
                event
            ) + ' is happening today! Get super pumped my home skillets! This event about to be straight bussin.'
            print(msg)
            msgObj = await client.get_channel(
                int(db["events"][event]["channel"])).send(msg)
            db["events"][event]["announced"] = msgObj.id
            print(db["events"][event])
