from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Room(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    r_id = models.AutoField(primary_key=True) 
    r_title = models.CharField(max_length=200)
    r_description = models.TextField(null=True, blank=True)
    r_participants = models.ManyToManyField(User, related_name= 'r_participants', blank=True)
    r_date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.r_title
    
    class Meta:
        ordering = ['-r_date_created']
    

class Message(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    rm_message = models.TextField()
    rm_date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-rm_date_created']

    def __str__(self):
        return self.rm_message[0:50]  
