from flask import Flask, request
import json
app = Flask(__name__)

contacts = [
    {"nom": "Martin", "id": 0},
    {"nom": "Gauthier", "id": 1},
    {"nom": "Clement", "id": 2},
    {"nom": "Romain", "id": 3}
    ]
    
all_messages = [
    {"receiver": 1, "sender": 0, "content": "Gauthier, tu ne seras jamais un vrai numero 1."},
    {"receiver": 1, "sender": 2, "content": "Je ne suis pas la pour le moment."},
    
    ]


@app.route('/send', methods=['GET'])
def send():
    content = request.args.get('message')
    receiver = request.args.get('to')
    sender = request.args.get('from')
    
    if content and receiver and sender:
        new_message = {'receiver': int(receiver), 'sender': int(sender), 'content': content}
        all_messages.append(new_message)
    
    return json.dumps(all_messages)


@app.route('/receive', methods=['GET'])  
def receive():
    receiver = request.args.get('to')
    messages_to_receiver = []
    
    """Find the messages sent to the receiver"""
    for message in all_messages:
        if message['receiver'] == int(receiver):
            sender = -1
            
            """Find the name of the sender"""
            for contact in contacts:
                if contact['id'] == message['sender']:
                    sender = contact['nom']
                    
            messages_to_receiver.append({'from': sender, 'message':message['content']})

    return json.dumps(messages_to_receiver)


@app.route('/clean')
def clean():
    all_messages = [
    {"receiver": 1, "sender": 0, "content": "Gauthier, tu ne seras jamais un vrai numero 1."}
    ]
    return json.dumps(all_messages)

@app.route('/hello')
def hello_world():
    return 'Hello hello !'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
