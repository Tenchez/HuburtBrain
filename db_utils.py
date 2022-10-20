import formats
import helper as h
import threading
from event import Event
from replit import db
from discord_const import client

threadLock = threading.Lock()


def insertEvent(event):
    events = db["events"]
    events[event.name] = {
        'where': event.where,
        'when': event.when,
        'hardDate': event.hardDate,
        'attendees': {},
        'id': event.id,
        'channel': event.channel,
        'announced': event.announced,
        'createdBy': event.createdBy
    }


def deleteEvent(name):
    if db['events'].get(name) != None:
        print(db['events'][name])
        eventData = db['events'].pop(name)
        return Event(eventData['id'], name, eventData['where'],
                     eventData['when'], eventData['hardDate'],
                     eventData['channel'], eventData['announced'],
                     eventData['createdBy'])
    else:
        return None


def convertToEvent(data) -> Event:
    event = Event(db["events"][data]['id'], data, db["events"][data]['where'],
                  db["events"][data]['when'], db["events"][data]['hardDate'],
                  db['events'][data]['channel'],
                  db['events'][data]['announced'],
                  db['events'][data]['createdBy'])
    event.attendees = db["events"][data]['attendees']
    return event


def getEvent(id):
    for e in db["events"]:
        if db["events"][e]['id'] == id:
            return convertToEvent(e)
    return None


def getEventList():
    events = []
    for e in db["events"]:
        events.append(convertToEvent(e))
    print(events)
    return events


def getEventListStr():
    events = db["events"]
    listMsg = "Events happening:\n"
    for key in events.keys():
        listMsg += "\t\t**Event**: " + key + " **where**: " + events[key][
            "where"] + " **when**: " + events[key][
                "when"] + " **date**: " + events[key][
                    "hardDate"] + " **Attending**: " + ", ".join(
                        events[key]["attendees"].values()) + "\n\n"
    return listMsg


async def updateEvent(name, when, where, hardDate):
    print(name + ' ' + when + ' ' + where + ' ' + hardDate)
    event = db['events'][name]
    when = when if when != '' else event['when']
    where = where if where != '' else event['where']
    hardDate = hardDate if hardDate != '' else event['hardDate']
    db['events'][name] = {
        'where': where,
        'when': when,
        'hardDate': hardDate,
        'attendees': event['attendees'],
        'id': event['id'],
        'channel': event['channel'],
        'announced': event['announced'],
        'createdBy': event['createdBy']
    }
    message = await client.get_channel(int(event["channel"])
                                       ).fetch_message(int(event['id']))
    await message.edit(content=formats.UPCOMING.format(
        name, db['events'][name]['where'], db['events'][name]['when'],
        db['events'][name]['hardDate'],len(db['events'][name]
                                                  ['attendees']), ', '.join(db['events'][name]
                                                  ['attendees'].values())))


def addEventAnnounced(name, id):
    db['events'][name]['announced'] = id


def addEventAttendee(event, username, id):
    threadLock.acquire(True)
    print("Lock acquired")
    try:
        print('adding username: ' + str(username) + " id: " + str(id))
        if str(id) not in event.attendees.keys():
            print("Added: " + str(id))
            db['events'][event.name]['attendees'][str(id)] = username
        return getEvent(event.id)
    finally:
        print("Lock released")
        threadLock.release()


def removeEventAttendee(event, id):
    threadLock.acquire(True)
    print("Lock acquired")
    event = getEvent(event.id)
    try:
        if str(id) in event.attendees.keys():
            print("Removed: " + str(id))
            event.attendees.pop(str(id))
            db['events'][event.name]['attendees'] = event.attendees
        return event
    finally:
        print("Lock released")
        threadLock.release()


async def updateAttending(message, event, user, emoji):
    if emoji == "☑":
        await message.remove_reaction(emoji, user)
        event = addEventAttendee(event, h.uidToName(user), user.id)
    elif emoji == "🇽":
        await message.remove_reaction(emoji, user)
        event = removeEventAttendee(event, user.id)
    print(event.attendees)
    await message.edit(content=formats.UPCOMING.format(
        event.name, event.where, event.when, event.hardDate,len(event.attendees), ', '.join(
            event.attendees.values())))
