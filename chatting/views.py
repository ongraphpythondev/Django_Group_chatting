from django.shortcuts import redirect, render
from django.contrib.auth.models import User

# Create your views here.


def index(request):
    if request.method == "GET":
        return render(request, 'chatting/index.html')

    if request.method == "POST":
        roomname = request.POST['room']
        username = request.POST['name']
        return redirect(f"{roomname}/{username}")


def room(request, room_name , user_name):
    return render(request, 'chatting/room.html', {
        'room_name': room_name,
        "user_name" : user_name
    })

def all_users(request):
    users_obj = User.objects.all()
    if not request.user.is_authenticated :
        return render(request, 'chatting/all_users.html', {
            "message" : "user must login"
        })
    return render(request, 'chatting/all_users.html', {
        "users" : users_obj
    })

def chat(request, user_name):
    if not request.user.is_authenticated :
        return render(request, 'chatting/all_users.html', {
            "message" : "user must login"
        })
    return render(request, 'chatting/chat.html', {
        "user_name" : user_name
    })