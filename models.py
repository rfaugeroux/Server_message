import datetime
from server_image import db

class Message(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    sender = db.StringField(max_length=255, required=True)
    receiver = db.StringField(max_length=255, required=True)
    content = db.StringField(required=True)

    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title

    meta = {
        'indexes': ['-created_at', 'receiver'],
        'ordering': ['-created_at']
    }


class User(db.Document):
    name = db.StringField(max_length=255, required=True)
    login = db.StringField(max_length=255, required=True)
    password = db.StringField(max_length=255, required=True)
