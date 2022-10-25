import asyncio
from datetime import date, datetime, time

from db.event import Event

def getTime():
    return datetime.now().strftime("%H:%M")


def getDate():
    return date.today().strftime("%m/%d/%Y")


async def checkTime():
    for event in Event.select():
        eventDate = datetime.strptime(event.date,"%m/%d/%Y").date()
        if eventDate == datetime.strptime(getDate(),"%m/%d/%Y").date() and datetime.now().time() >= time(8,00):
            await event.announce()
        if eventDate < datetime.strptime(getDate(),"%m/%d/%Y").date():
            await event.remove()
    await asyncio.sleep(60*10)#10 minutes
