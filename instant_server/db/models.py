# -*-coding:Utf-8 -*
from mongoengine import Document, StringField, DateTimeField, EmailField, BooleanField, IntField
from mongoengine import connect  # , register_connection
from auth_server.db.models import User

import datetime


PRODUCTION_URI = 'mongodb://keo_user:GMRJ4keo@ds027338.mongolab.com:27338/keo'
#PRODUCTION_ALIAS = 'keo-local'  # 'keo-production'


print "connecting to keo-database..."
#register_connection(PRODUCTION_ALIAS, 'instant-server-production', host=PRODUCTION_URI)

connect('keo', host=PRODUCTION_URI)


class Message(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    delivery_time = DateTimeField(default=datetime.datetime.now, required=True)
    keo_time = IntField(min_value=0, default=0, required=True)
    sender = StringField(max_length=255, required=True)
    receiver = StringField(max_length=255, required=True)
    content = StringField(required=True)
    delivered = BooleanField(default=False, required=True)
    photo = StringField(required=False)


    meta = {
        'indexes': ['-created_at', 'receiver'],
        'ordering': ['-delivery_time']
    }


class Global_User(User):
    last_update = DateTimeField(default=datetime.datetime.min,required=True)
    os = StringField(max_length=255, required=True)
    reg_id = StringField(max_length=255, default=None, required=True)
    
