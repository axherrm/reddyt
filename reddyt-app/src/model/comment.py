import datetime
from peewee import *

from ..db_service import DBService
from .post import Post

class Comment(Model):

    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    post = ForeignKeyField(Post, backref='comments')

    class Meta:
        database = DBService.connection