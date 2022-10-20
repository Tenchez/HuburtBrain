class Event:
   'Common base class for all events'
   empCount = 0
   def __init__(self, id, name, where, when, hardDate, channel, announced, createdBy):
      print("Event: {}".format(id))
      self.id = id
      self.name = name
      self.when = when
      self.where = where
      self.hardDate = hardDate
      self.channel = channel
      self.attendees = {}
      self.outsideAttendees = []
      self.announced = announced
      self.createdBy = createdBy

   def toString(event):
      print('name: ' + event.name + " when: " + event.when + ' where: ' + event.where + ' date: ' + event.hardDate + ' channel: ' + str(event.channel) + ' id: ' + str(event.id) + ' announced: ' + str(event.announced) + ' attendees: ' + ', '.join(event.attendees.values()) + ' createdBy: ' + str(event.createdBy))
