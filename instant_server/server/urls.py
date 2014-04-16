import json
import datetime
from flask import request
from instant_server.server import app
from instant_server.db import models


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


@app.route('/hello')
def hello_world():
    return 'Hello Hello'

@app.route('/testPost', methods=['GET', 'POST'])
def testPost():
    print "On est au debut"
    print json.dumps(request.form)
    print "On est a la fin"
    return "Post tested"

