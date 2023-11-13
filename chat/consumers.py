import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from accounts.models import User
from .models import Message, ChatRoom, UserStatus


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_slug = self.scope['url_route']['kwargs']['room_slug']
        self.room_group_name = f'chat_{self.room_slug}'
        self.sender = self.scope['user']

        # Update user status to online when connect happens.
        user_status, _ = await sync_to_async(UserStatus.objects.get_or_create)(user=self.scope['user'])
        user_status.online = True
        await sync_to_async(user_status.save)()
        

        # Add the sender to the seen_by field of all messages in the chat room
        self.chat_room = await sync_to_async(ChatRoom.objects.get)(slug=self.room_slug)
        messages = await sync_to_async(Message.objects.filter)(chat_room=self.chat_room)
        async for message in messages:
            await sync_to_async(message.seen_by.add)(self.sender)


        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

   

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
       
        # Get user status
        online = await sync_to_async(UserStatus.objects.get)(user=self.sender)

        # Create an object of message
        message_obj = await sync_to_async(Message.objects.create)(chat_room=self.chat_room, sender=self.sender, message=message)
        
        # add user to list of seen by users and create a list of usernames
        seen_by_users = await sync_to_async(message_obj.seen_by.all)()
        seen_by_usernames = await sync_to_async(lambda: [user.username for user in seen_by_users])()

        # Notify the group about the new message
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_room_message',
                'message': str(message),
                'username': self.sender.username,
                'online': online.is_online() if online else False, 
                'seen_by': seen_by_usernames, 
            }
        )


    async def chat_room_message(self, event):
        message = event['message']
        username = event['username']
        online = event['online']
        seen_by = event['seen_by']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'online': online, 
            'seen_by': seen_by
        }))
        

    async def user_status(self, event):
        username = event['username']
        online = event['online']

        await self.send(text_data=json.dumps({
            'username': username,
            'online': online
        }))


    async def disconnect(self, code):
        # Get user status and change it to offline when disconnect happens  
        user_status, _ = await sync_to_async(UserStatus.objects.get_or_create)(user=self.sender)
        user_status.online = False
        await sync_to_async(user_status.save)()


        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'username': self.sender.username,
                'online': False
            }
        )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )