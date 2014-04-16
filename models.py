import datetime
from server_image import db

class Message(db.Document):
    sent_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    reception_date = db.DateTimeField(default=datetime.datetime.now, required=True)
    sender = db.StringField(max_length=255, required=True)
    receiver = db.StringField(max_length=255, required=True)
    content = db.StringField(required=True)

    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    meta = {
        'indexes': ['-sent_at', 'receiver'],
        'ordering': ['-sent_at']
    }


class User(db.Document):
    name = db.StringField(max_length=255, required=True)
    phone_number = db.StringField(max_length=255, required=True)
    email = db.EmailField(required=True)
    login = db.StringField(max_length=255, required=True)
    password = db.StringField(max_length=255, required=True)
