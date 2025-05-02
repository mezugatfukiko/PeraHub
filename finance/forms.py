from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class CustomRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 text-sm rounded-md border border-gray-300 mt-1',
        }),
        label="Username"
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 text-sm rounded-md border border-gray-300 mt-1',
        }),
        label="First Name"
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 text-sm rounded-md border border-gray-300 mt-1',
        }),
        label="Last Name"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full p-2 text-sm rounded-md border border-gray-300 mt-1',
        }),
        label="Email Address"
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-2 text-sm rounded-md border border-gray-300 mt-1',
        }),
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-2 text-sm rounded-md border border-gray-300 mt-1',
        }),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

        
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-2 text-sm rounded-md border border-gray-300 mt-1',
        # 'placeholder': 'Enter your username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full p-2 text-sm rounded-md border border-gray-300 mt-1',
        # 'placeholder': 'Enter your password'
    }))