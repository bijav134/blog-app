from django import forms
from django.forms import fields, models
from blog import models


class UserModelForm(forms.ModelForm):
    class Meta():
        model = models.User
        fields = ('username','email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta():
        model = models.UserProfile
        exclude = ('user',)


class PostModelForm(forms.ModelForm):
    class Meta():
        model=models.Post
        fields=('author','title','text')


class CommentModelForm(forms.ModelForm):
    class Meta():
        model=models.Comment
        fields= ('author','text')