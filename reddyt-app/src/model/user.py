from peewee import *

from ..db_service import DBService


class User(Model):

    username = CharField(unique=True, primary_key=True)
    last_name = CharField()
    first_name = CharField()
    email = CharField()

    class Meta:
        database = DBService.connection