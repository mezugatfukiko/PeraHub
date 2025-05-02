from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm  # <-- import your custom form here
from .forms import CustomRegisterForm
from django.contrib.auth.decorators import login_required



def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in
            return redirect('dashboard')  # Redirect to dashboard after registration
    else:
        form = CustomRegisterForm()
    return render(request, 'finance/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()

    return render(request, 'finance/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # after logout, go back to login
    
@login_required
def dashboard_view(request):
    return render(request, 'finance/dashboard.html')  # You can change the path if needed