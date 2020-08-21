from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    room = models.TextField(max_length=100)
    room_description = models.TextField(max_length=100, null=True)

    def __str__(self):
        return self.room


class Message(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.author.username

    def messages_on_load(self, room):
        return Message.objects.filter(room__room=room).order_by('-timestamp').all()[:10]

    def conversation_history(self, room, msg_limit_from, msg_limit_to):
        return Message.objects.filter(room__room=room).order_by('-timestamp').all()[msg_limit_from:msg_limit_to]
