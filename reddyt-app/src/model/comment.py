import datetime
from peewee import *

from ..db_service import DBService
from .post import Post
from .user import User

class Comment(Model):

    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    post = ForeignKeyField(Post, backref='comments')
    user = ForeignKeyField(User)

    class Meta:
        database = DBService.connection