from django import forms
from .models import Room
from django.contrib.auth.models import User

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['user', 'r_participants']
        widgets = {
            'r_title': forms.TextInput(attrs={'placeholder': 'Enter Room Title'}),
            'r_description': forms.Textarea(attrs={'placeholder': 'Enter Room Description'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

