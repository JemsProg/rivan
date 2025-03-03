from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),



    path('', views.landingPage, name="landing"),
    path('course/', views.landingCourse, name="landingCourse"),
    path('about/', views.landingAbout, name="landingAbout"),



    path('home/', views.home, name="home"),
    path('notification/', views.notificationPage, name="notification"),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('update-profile/', views.updateProfile, name='update-profile'),




    path('room/<str:pk>/', views.room, name='room'),    
    path('create-room/', views.createRoom, name='create-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),

    path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),




]