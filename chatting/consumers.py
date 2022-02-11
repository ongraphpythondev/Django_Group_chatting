import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Connection , Message



class PersonalChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user_name = self.scope['url_route']['kwargs']['user_name']
        self.user = self.scope["user"]
        if not self.user.is_authenticated :
            print("user is not authenticated")
        self.other_user = User.objects.filter(username = self.user_name).first()
        if not self.user.is_authenticated :
            print("other user is not authenticated")
        
        self.connection_obj = Connection.get_or_create_room_id(self.user , self.other_user)
        self.room_group_name = self.connection_obj.connection_id
        

        print(self.connection_obj.message.all().order_by('created_at'))

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        self.all_messages = self.connection_obj.message.all().order_by('created_at')
        self.send(text_data=json.dumps({"status": "connected woow" } ))
        
        if self.all_messages:
            for message in self.all_messages:
                print("hh")
                data = {
                    "username" : message.sender.username,
                    "message" : message.message
                }
                self.send(text_data=json.dumps({
                    'data': data
                    } ))
    	

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        """
        It run when some consumer send message not on receive
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        data = {
            "username" : self.user.username,
            "message" : message
        }

        # this method save the message to db
        self.save_message(message)


        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'data': data
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        """
        It run on sending or receiving message
        """
        data = event['data']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'data': data,
        }))

    def save_message(self , message : str):
        message_obj = Message.objects.create(connection = self.connection_obj, sender = self.user , receiver = self.other_user , message = message)
        message_obj.save()
        

class GroupChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user_name = self.scope['url_route']['kwargs']['user_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print(self.room_group_name , self.channel_name , self.scope["user"])
        # Join room group
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
        """
        It run when some consumer send message not on receive
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        message = self.user_name + " : " + message

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        """
        It run on sending or receiving message
        """
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

