import json
import datetime
from flask import request
from instant_server.server import app
from instant_server.db import models
from mongoengine.queryset import DoesNotExist


@app.route('/send', methods=['POST'])
def send():

    content = request.form['message']
    receiver = request.form['to']
    sender = request.form['from']

    
    if content and receiver and sender:
        message = models.Message(sender=sender, receiver=receiver, content=content)
        message.save()

    return "Message sent !"


@app.route('/receive', methods=['GET'])
def receive():
    receiver = request.args.get('to')
    messages_to_receiver = []

    """Collect the messages sent to the receiver"""
    for message in models.Message.objects(receiver=receiver):
        messages_to_receiver.append({'from': message.sender, 'message': message.content})

    return json.dumps(messages_to_receiver)


@app.route('/delete', methods=['GET'])
def delete():
    t = datetime.timedelta(minutes=2)
    time_barrier = datetime.datetime.now() - t
    models.Message.objects(created_at__lte=time_barrier).delete()
    return "Messages created more than 2 minutes ago deleted."

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']
    phone_number = request.form['phone_number']

    if models.Global_User.objects(email=email):
        return "false"

    new_user = models.Global_User(email=email, phone_number=phone_number, password=password)
    new_user.save()

    return "true"

@app.route('/login', methods=['POST'])
def login():
    print "debut"
    email = request.form['email']
    password = request.form['password']

    try:
        user = models.User.objects.get(email=email, password=password)
        print user.phone_number
        return user.phone_number
    except DoesNotExist:
        return "DoesNotExist"
         
    return "NTM"

@app.route('/users', methods=['GET'])
def get_users():
    users = []
    for user in models.Global_User.objects:
        users.append({'email': user.email, 'phone number': user.phone_number, 'password': "*******"})
    return json.dumps(users)



@app.route('/hello')
def hello_world():
    return 'Hello Hello'

