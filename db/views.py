from peewee import *

db = SqliteDatabase('db/data/views.db')


class Views(Model):
    id = AutoField(primary_key=True, unique=True)
    guild = IntegerField()
    type = IntegerField()
    channel = IntegerField()
    message = IntegerField(unique=True)

    class Meta:
        database = db


def initialize_db():
    db.connect()
    db.create_tables([Views], safe=True)
    db.close()


initialize_db()
