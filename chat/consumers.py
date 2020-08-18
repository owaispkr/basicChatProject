import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, Room
from django.contrib.auth import get_user_model
from .models import Message


User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def fetch_message(self, room):
        messages = Message.last_10_messages(self, room)
        content = {
            'command': 'previous_messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id': message.id,
            'message': message.content,
            'author': message.author.username,
            'timestamp': str(message.timestamp)
        }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['command'] == "previous_messages":
            self.fetch_message(text_data_json['room'])

        else:
            message = text_data_json['message']
            author = text_data_json['from']
            room_name = text_data_json['room']
            author_user = User.objects.filter(username=author)[0]
            room = Room.objects.filter(room=room_name)[0]
            m = Message(author=author_user, content=message, room=room)
            m.save()

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'author_user': author,
                    'msgtime': ''
                }
            )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        author = event['author_user']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'command': 'new_messages',
            'message': message,
            'author': author
        }))
