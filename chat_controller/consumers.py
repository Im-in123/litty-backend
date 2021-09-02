from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.generic.websocket import WebsocketConsumer
from .models import ChatList, Message
from user_controller.models import CustomUser
from asgiref.sync import async_to_sync
from django.db.models import Q


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        print('Fetch:::', data)
        messages = Message.objects.order_by('-created_at').all()[:5]

        user = data['username']
        other_user = data['other_person']
        user= CustomUser.objects.get(username= user)
        other_user= CustomUser.objects.get(username= other_user)
        try:
            check = ChatList.objects.get(user=user, other=other_user)
        except Exception as e:
            print("fetch error:::", e)
            check =ChatList.objects.create(user=user, other=other_user)
            


        print("fetch user::",user)
        print("otheruser::",other_user)

        queryset = Message.objects.select_related(
        "sender", "receiver")
        print("queryset::",queryset)
        print("..")
        qs = queryset.filter(Q(sender=user, receiver=other_user) | Q(
                 sender=other_user, receiver=user))[:5]
        # qs = queryset.filter(Q(sender_id=user_id, receiver_id=active_user_id) | Q(
        #          sender_id=active_user_id, receiver_id=user_id))
        print("qs:::", qs)
        print("..")
        content = {
            'command':'messages',
            'messages':self.messages_to_json(qs),
        }
        self.send_message(content)

    def new_message(self, data):
        print('New message:::', data)
        author = data['from']
        to = data['to']
        author_user = CustomUser.objects.filter(username = author)[0]
        to_user= CustomUser.objects.get(username= to)
        message = Message.objects.create(sender = author_user, receiver = to_user, message= data['message'])
        content = {
            'command': 'new_message', 
            'message':  self.message_to_json(message)
        }
        
        # print("new message content::", content)
        return  self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id': message.id,
            'sender': message.sender.username,
            'message': message.message,
            'timestamp':str(message.created_at)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

 

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()


    def disconnect(self, close_code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("Disconected")


    # Receive message from WebSocket
    def receive(self, text_data):
        print("receive:::", text_data)
        data = json.loads(text_data)
        print("receive data:::", data)
        self.commands[data['command']](self,data)

    def send_chat_message(self, message):
        print("send_chat_message:::", message)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )


    def send_message(self, message):
        print("sendmessagecustom::",message)
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        print("chat_message:::", event)
        message = event['message']
        self.send(text_data=json.dumps(message))