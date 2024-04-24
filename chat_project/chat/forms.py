from django import forms
from .models import Room, Profile


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name','slug',]


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture']
