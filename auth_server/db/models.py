# -*-coding:Utf-8 -*
from mongoengine import Document, StringField, DateTimeField, EmailField, BooleanField

class User(Document):
    phone_number = StringField(max_length=255, required=True)
    email = EmailField(required=True)
    password = StringField(max_length=255, required=True)
