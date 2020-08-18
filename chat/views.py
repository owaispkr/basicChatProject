from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
from .models import Room, Message
import json

@login_required
def index(request):
    # room = list(Room.objects.all().values('room'))
    room = list(Room.objects.all().values('room'))
    print(room)
    #return render(request, 'chat/index.html', {'room': mark_safe(json.dumps(room))})
    return render(request, 'chat/index.html', {'room': room})

@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
    })

@login_required
def chatroom(request, room_name):
    print("agaya")
    return render(request, 'chat/chatroom.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
    })