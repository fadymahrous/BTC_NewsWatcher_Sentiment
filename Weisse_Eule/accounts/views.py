from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_user(request):
    """
    Handles user login.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('trade_augur:home_page')
        else:
            messages.info(request, "If you don't have an account, please use the link below to create one.")
            return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

def create_user(request):
    """
    Handles user registration with a custom user creation form.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully.")
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'Create_user.html', {'form': form})

@login_required
def logout_user(request):
    """
    Logs out the current user.
    """
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('accounts:login')
