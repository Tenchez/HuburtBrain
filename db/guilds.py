from peewee import *

db = SqliteDatabase('db/data/guilds.db')


class Guilds(Model):
    guild = IntegerField(primary_key=True, unique=True)
    channel = IntegerField()

    class Meta:
        database = db


def initialize_db():
    db.connect()
    db.create_tables([Guilds], safe=True)
    db.close()


initialize_db()
