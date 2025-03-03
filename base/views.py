from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Message, Topic
from .forms import RoomForm, UserForm


#landingPage view to display landingpage
def landingPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    return render(request, 'landing_base.html')

#landingPage view to display landingpage course
def landingCourse(request):    
    return render(request, 'landing_course.html')

#landingPage view to display landingpage about
def landingAbout(request):    
    return render(request, 'landing_about.html')

def notificationPage(request):
    room_message = Message.objects.all()
    
    context = {'room_message': room_message}
    # if request.user.is_authenticated:
    #     return redirect('home')
    
    return render(request, 'base/notification.html', context)


#loginPage view to display login
def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not match')

    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('landing')  

#registerPage view to display register
def registerPage(request):
    form = UserCreationForm()

    if request.method  == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form':form})

# Home view to display all rooms
@login_required(login_url='login')
def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms} 
    return render(request, 'base/discussion.html', context)

# Room details view
@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(r_id=pk)
    rm_meesage = room.message_set.all().order_by('-rm_date_created')
    r_participants = room.r_participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            rm_message = request.POST.get('rm_message')
        )
        room.r_participants.add(request.user)
        return redirect('room', pk=room.r_id)

    context = {'room': room, 'rm_meesage':rm_meesage, 'participants':r_participants}
    return render(request, 'base/discussion_room.html', context)

#view of profile
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms =  user.room_set.all()
    context = {'user':user, 'rooms':rooms}
    return render(request, 'base/profile.html', context)

# View to create a new room
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(title=topic_name)
        
        Room.objects.create(
            user = request.user,
            topic = topic,
            r_title = request.POST.get('r_title'),
            r_description = request.POST.get('r_description'),

        )
  
        return redirect('home')  # Change 'home' to any other URL if needed
    context = {'form': form, 'topics':topics}
    return render(request, 'base/create_room.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(r_id=pk)

    if request.user != room.user:
        return HttpResponse('You are now allowed here.')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are now allowed here.')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})


@login_required(login_url='login')
def updateProfile(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)    

    return render(request, 'base/update_profile.html', {'form':form})