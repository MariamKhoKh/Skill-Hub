from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User,  Message


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput())
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLES)

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'profile_picture')


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']