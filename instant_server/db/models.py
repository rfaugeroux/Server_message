# -*-coding:Utf-8 -*
from mongoengine import Document, StringField, register_connection, DateTimeField
from flask import url_for
import datetime


PRODUCTION_URI = ''  # TODO change this for actual db
PRODUCTION_ALIAS = ''

print "connecting to question-tree database"
register_connection(PRODUCTION_ALIAS, 'instant-server-production', host=PRODUCTION_URI)


class Message(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    sender = StringField(max_length=255, required=True)
    receiver = StringField(max_length=255, required=True)
    content = StringField(required=True)

    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title

    meta = {
        'indexes': ['-created_at', 'receiver'],
        'ordering': ['-created_at']
    }


class User(Document):
    name = StringField(max_length=255, required=True)
    login = StringField(max_length=255, required=True)  # TODO -> use authentification server...
    password = StringField(max_length=255, required=True)
