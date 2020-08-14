from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    room = models.TextField(max_length=100)

    def __str__(self):
        return self.room


class Message(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.author.username

    def last_10_messages(self):
        return Message.objects.order_by('-timestamp').all()[:10]
