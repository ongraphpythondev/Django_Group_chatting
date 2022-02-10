from django.shortcuts import redirect, render

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