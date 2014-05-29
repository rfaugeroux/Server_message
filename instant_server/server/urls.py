import json
import datetime
from flask import request
from instant_server.server import app
from instant_server.db import models
from mongoengine.queryset import DoesNotExist
from mongoengine import ValidationError
from gcm import GCM
from gcm.gcm import GCMException
#from apnsclient import Message, APNs

GCM_API_KEY = "AIzaSyCWn_dNhBHFITuVAOAG2r_KDlV5KROg-Oo"
passphrase = "NapoleonGrouchy"


@app.route('/send', methods=['POST'])
def send():

    content = request.form['message']
    receiver_id = request.form['to']
    sender = request.form['from']
    minutes = request.form.get('delivery_time', default=0, type=int)

    delta = datetime.timedelta(minutes = minutes)

    message = models.Message(sender=sender, receiver=receiver_id, 
                             content=content, delivery_time=datetime.datetime.now() + delta)
    message.save()
    print "Message id: " + str(message.id)

    user = models.Global_User.objects.get(email=receiver_id)

    if user.reg_id and minutes < 1:
        if user.os=="android":
            gcm = GCM(GCM_API_KEY)
            data = {'sender' : sender, 'id': str(message.id)}         
            print data
            try:
                res = gcm.plaintext_request(registration_id=user.reg_id, data=data)
            except GCMException, e:
                print e

        if user.os=="ios" and False:
            con = Session.new_connection("push_sandbox", cert_file="ck.pem", passphrase=passphrase)
            message = Message([user.reg_id], alert="Une seule notif", badge=1)
            srv = APNs(con)
            res = srv.send(message)
            # Check failures. Check codes in APNs reference docs.
            for token, reason in res.failed.items():
                code, errmsg = reason
                print "Device failed: {0}, reason: {1}".format(token, errmsg)

            # Check failures not related to devices.
            for code, errmsg in res.errors:
                print "Error: ", errmsg

            # Check if there are tokens that can be retried
            if res.needs_retry():
                # repeat with retry_message or reschedule your task
                retry_message = res.retry()

    return "Message sent"


@app.route('/receive', methods=['GET'])
def receive():
    receiver = request.args.get('to')
    #timestamp = request.args.get('timestamp')

    timestamp = datetime.datetime.now() - datetime.timedelta(weeks=15)

    messages_to_receiver = []

    """Collect the messages sent to the receiver"""
    for message in models.Message.objects(receiver=receiver, delivery_time__lte=datetime.datetime.now(),
                                          delivery_time__gte=timestamp):
        messages_to_receiver.append({'from': message.sender, 'message': message.content,
                                     'created_at': str(message.created_at)})

    return json.dumps(messages_to_receiver)

@app.route('/receive_single', methods=['GET'])
def receive_single():
    id = request.args.get('id')
    messages_to_receiver = []

    """Collect the message requested by the receiver"""
    message  = models.Message.objects.get(id=id)
    messages_to_receiver.append({'from': message.sender, 'message': message.content,
                                 'created_at': str(message.created_at)})

    return json.dumps(messages_to_receiver)

@app.route('/delete', methods=['GET'])
def delete():
    t = datetime.timedelta(minutes=3)
    time_barrier = datetime.datetime.now() - t
    models.Message.objects(receiver="", delivery_time__lte=time_barrier).delete()
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

