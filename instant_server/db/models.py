# -*-coding:Utf-8 -*
from mongoengine import Document, StringField, DateTimeField, EmailField, BooleanField
from mongoengine import connect  # , register_connection

from flask import url_for
import datetime


PRODUCTION_URI = 'mongodb://keo_user:GMRJ4keo@ds027338.mongolab.com:27338/keo'  # change this to production URI
#PRODUCTION_ALIAS = 'keo-local'  # 'keo-production'


print "connecting to keo-database..."
#register_connection(PRODUCTION_ALIAS, 'instant-server-production', host=PRODUCTION_URI)

connect('keo', host=PRODUCTION_URI)


class Message(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    sender = StringField(max_length=255, required=True)
    receiver = StringField(max_length=255, required=True)
    content = StringField(required=True)
    delivered = BooleanField(default=False, required=True)


    meta = {
        'indexes': ['-created_at', 'receiver'],
        'ordering': ['-created_at']
    }


class User(Document):
    phone_number = StringField(max_length=255, required=True)
    email = EmailField(required=True)
    login = StringField(max_length=255, required=True)  # TODO -> use authentification server...
    password = StringField(max_length=255, required=True)
