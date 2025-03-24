from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import News, Comment



class UserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ["username", "password"]


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "content"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]  
        widgets = {"content": forms.Textarea(attrs={"rows": 4})}
        labels = {"content": ""} 


class EditNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "content"]