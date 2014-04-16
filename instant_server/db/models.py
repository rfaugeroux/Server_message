# -*-coding:Utf-8 -*
from mongoengine import Document, StringField, DateTimeField
from mongoengine import connect  # , register_connection

from flask import url_for
import datetime


#PRODUCTION_URI = 'mongodb://localhost:27020/mydb'  # change this to production URI
#PRODUCTION_ALIAS = 'keo-local'  # 'keo-production'


print "connecting to keo-database..."
#register_connection(PRODUCTION_ALIAS, 'instant-server-production', host=PRODUCTION_URI)

connect('keo')


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
