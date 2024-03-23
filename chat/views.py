from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login,logout,authenticate
from .models import My_User
import requests



# Create your views here.
def home(request):
    return render(request, 'home.html')



def login(request):
    if request.user.is_authenticated:
        return redirect('/check/')
    
    else :
        if request.method=='POST':
            uname=request.POST['username']
            upass=request.POST['password']
            userTemp=My_User.objects.get(username=uname,password=upass)
            print(userTemp)
            user=authenticate(username=uname,password=upass)
            print(user)
            if user is not None:
                login(request,userTemp)
                return redirect('/check/')

        else:
            print('error')
        return render(request,'login.html')

def check(request):
    return render(request,'check.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    # new_message.save()
   

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})

def weather(request):
    if 'city' in request.POST:
        city=request.POST['city']
        # print(city)
    else :
        city='Dhaka'
        
    appid='30366edea2c8585b1f1ca3825ac895d3'
    URL='https://api.openweathermap.org/data/2.5/weather'
    PARAMS={
        'q':city,
        'appid':appid,
        'units':'metric',
        }
    r=requests.get(url=URL,params=PARAMS)
    res=r.json()
    context={
        'description':res['weather'][0]['description'].capitalize(),
        'icon':res['weather'][0]['icon'],
        'temp':res['main']['temp'],
        'feels_like':res['main']['feels_like'],
        'temp_min':res['main']['temp_min'],
        'temp_max':res['main']['temp_max'],
        'pressure':res['main']['pressure'],
        'humidity':res['main']['humidity'],
        'wind':res['wind']['speed'],
        'clouds':res['clouds']['all'],
        'city':city.capitalize(),
        'country':res['sys']['country'],
        
        
        }

    return render(request,'home1.html',context)