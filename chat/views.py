from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import ChatRoom, Message
from django.views.generic import View, UpdateView
from .forms import CreateChatRoomForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User



def get_chat_rooms_with_last_message():
    chat_rooms = ChatRoom.objects.all()
    chat_rooms_with_last_message = []

    for room in chat_rooms:
        last_message = Message.objects.filter(chat_room=room).order_by('-created_at').first() 

        chat_rooms_with_last_message.append({
            'id': room.id,
            'room_name': room.name,
            'room_slug': room.slug,
            'last_message': {
                'message': last_message.message if last_message else None,
                'created_at': last_message.get_created_at if last_message else None,
                'sender': last_message.sender.username if last_message and last_message.sender else None
            }
        })

    return chat_rooms_with_last_message



def room(request, slug):
    chat_room = get_object_or_404(ChatRoom, slug=slug)
    chat_messages = Message.objects.filter(chat_room=chat_room)

    context = {
        'room_name': chat_room.name,
        'room_slug': chat_room.slug, 
        'chat_messages': chat_messages,
        'current_user': request.user.username
    }


    return render(request, 'chat/chat_room.html', context)




class CreateChatRoomView(LoginRequiredMixin, View):
    template_name = 'chat/index.html'
    form_class = CreateChatRoomForm
    

    def get(self, request, *args, **kwargs):
        chat_rooms = get_chat_rooms_with_last_message()
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'chat_rooms': chat_rooms})

    
    def post(self, request, *args, **kwargs):
        chat_rooms = get_chat_rooms_with_last_message()
        form = self.form_class(request.POST)
        if form.is_valid():
            room_name = form.cleaned_data['name']
            chat_room, created = ChatRoom.objects.get_or_create(name=room_name)
            return redirect(chat_room.get_absolute_url())
        return render(request, self.template_name, {'form': form, 'chat_rooms': chat_rooms, 'room_name': room_name})


