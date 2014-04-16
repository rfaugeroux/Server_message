# Set the path
import os, sys
import json
import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import request
from flask.ext.script import Manager, Server
from server_image import app, db
from server_image.models import Message

manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0')
)

@app.route('/send', methods=['POST'])
def send():
    content = request.form['message']
    receiver = request.form['to']
    sender = request.form['from']
    
    if content and receiver and sender:
        message = Message(sender= sender, receiver = receiver, content = content)
        message.save()
    
    return "Message sent !"


@app.route('/receive', methods=['GET'])  
def receive():
    receiver = request.args.get('to')
    messages_to_receiver = []
    
    """Collect the messages sent to the receiver"""
    for message in Message.objects(receiver=receiver):
        messages_to_receiver.append({'from': message.sender, 'message':message.content})

    return json.dumps(messages_to_receiver)


@app.route('/delete', methods=['GET'])
def delete():
    t = datetime.timedelta(minutes=2)
    time_barrier = datetime.datetime.now() - t
    Message.objects(created_at__lte=time_barrier).delete()
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

if __name__ == "__main__":
    manager.run()
