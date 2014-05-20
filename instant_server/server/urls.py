import json
import datetime
from flask import request
from instant_server.server import app
from instant_server.db import models
from mongoengine.queryset import DoesNotExist
from mongoengine import ValidationError


@app.route('/send', methods=['POST'])
def send():

    content = request.form['message']
    receiver = request.form['to']
    sender = request.form['from']
    minutes = request.form.get('delivery_time', default=0, type=int)

    delta = datetime.timedelta(minutes = minutes)

    message = models.Message(sender=sender, receiver=receiver, 
                             content=content, delivery_time=datetime.datetime.now() + delta)
    message.save()

    return "Message sent"


@app.route('/receive', methods=['GET'])
def receive():
    receiver = request.args.get('to')
    timestamp = request.args.get('timestamp')

    messages_to_receiver = []

    if timestamp > datetime.datetime.now():
        return "['Wrong timestamp: in the future']"

    """Collect the messages sent to the receiver"""
    for message in models.Message.objects(receiver=receiver, delivery_time__lte=datetime.datetime.now(),
                                          delivery_time__gte=timestamp):
        messages_to_receiver.append({'from': message.sender, 'message': message.content,
                                     'created_at': str(message.created_at)})

    return json.dumps(messages_to_receiver)


@app.route('/delete', methods=['GET'])
def delete():
    t = datetime.timedelta(minutes=2)
    time_barrier = datetime.datetime.now() - t
    models.Message.objects(created_at__lte=time_barrier).delete()
    return "Messages created more than 2 minutes ago deleted."

@app.route('/checkAccount', methods=['GET'])
def checkAccount():
    email = request.args.get('email')
    if models.Global_User.objects(email=email):
        return 'existe_deja'
    else:
        return 'continue'

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']
    phone_number = request.form['phone_number']
    os = request.form['os']
    reg_id = request.form.get('reg_id', default=None)


    if models.Global_User.objects(email=email):
        return "existe_deja"

    try:
        new_user = models.Global_User(email=email, phone_number=phone_number, password=password, os=os, reg_id=reg_id)
        new_user.save(validate=False)
        return "cree"

    except ValidationError, e:
        print e

    return "pas_cree"

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    os = request.form['os']
    reg_id = request.form.get('reg_id', default=None)

    try:
        user = models.User.objects.get(email=email, password=password)
        user.os = os
        if reg_id:
            user.reg_id = reg_id
        user.save()

        return user.phone_number
    
    except DoesNotExist:
        return "DoesNotExist"
         
    return "NTM"

@app.route('/sendRegId', methods=['POST'])
def sendRegId():
    reg_id = request.form['reg_id']



@app.route('/users', methods=['GET'])
def get_users():
    users = []
    for user in models.Global_User.objects:
        users.append({'email': user.email, 'phone number': user.phone_number, 'password': "*******"})
    return json.dumps(users)



@app.route('/hello')
def hello_world():
    return 'Hello Hello'

