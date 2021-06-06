import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from core.serializers import MessageSerializer, MessageOutputSerializer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['subject_id']
        self.room_group_name = f'chat_{self.room_name}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text_data_json.update({
            'author': self.scope['user'].id,
            'subject': self.scope['url_route']['kwargs']['subject_id'],
        })
        serializer = MessageSerializer(data=text_data_json)
        message = '*****'
        if serializer.is_valid():
            message = serializer.create(serializer.validated_data)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': MessageOutputSerializer(message).data
            }
        )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
