import formats
import helper as h
import db_utils

from event import Event


async def createMethod(creator, upcomingChannel, channel, name, where, when,
                       hardDate):
    upcoming = await upcomingChannel.send(
        formats.UPCOMING.format(name, where, when, hardDate, 0, []))
    print('upcoming id:' + str(upcoming.id) + ' by: ' + str(creator))
    event = Event(upcoming.id, name, where, when, hardDate, upcomingChannel.id,
                  False, str(creator))
    db_utils.insertEvent(event)
    await h.message(
        channel,
        "Hooray! Event created: " + name + " for: " + when + " at: " + where)
    await h.addReaction(upcoming, "☑")
    await h.addReaction(upcoming, "🇽")
    print("New event created: {}".format(upcoming.id))


async def deleteMethod(name, context=None, interaction=None, respond=True):
    event = db_utils.deleteEvent(name)
    if (event != None):
        await h.cleanUpMessages(event)
        if respond:
            if (interaction is not None):
                await h.respond(interaction,
                                "Removed " + name + " from the event list.",
                                True)
            elif (context is not None):
                await h.message(context,
                                "Removed " + name + " from the event list.")
    else:
        if respond:
            if (interaction is not None):
                await h.respond(interaction, "Event doesn't exist.", True)
            elif (context is not None):
                await h.message(context, "Event doesn't exist.")
