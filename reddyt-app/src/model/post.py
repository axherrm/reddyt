import datetime

from peewee import *
from .user import User

from ..db_service import DBService

class Post(Model):

    title = TextField()
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(User)

    class Meta:
        database = DBService.connection