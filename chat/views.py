from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
from .models import Room
import json

def index(request):
    room = Room.objects.all()
    room_obj = []
    for r in room:
        room_obj.append(str(r.room))
    return render(request, 'chat/index.html', {'room': json.dumps(room_obj)})

@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
    })