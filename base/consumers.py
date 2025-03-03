import os
import django
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

# Ensure Django is loaded properly before using models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rivan.settings")
django.setup()

from django.contrib.auth.models import User
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Add user to the WebSocket group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Remove user from the WebSocket group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        username = data.get('username')

        if not message or not username:
            return  # Prevent empty messages

        try:
            user = await sync_to_async(User.objects.get)(username=username)
            room = await sync_to_async(Room.objects.get)(r_id=self.room_name)

            # Save message to database
            await sync_to_async(Message.objects.create)(
                user=user,
                room=room,
                rm_message=message
            )

            # Broadcast message to group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username
                }
            )

        except User.DoesNotExist:
            print(f"User {username} not found")
        except Room.DoesNotExist:
            print(f"Room {self.room_name} not found")

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
