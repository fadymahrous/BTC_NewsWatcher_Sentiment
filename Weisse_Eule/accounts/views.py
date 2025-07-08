from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from .forms import CustomUserCreationForm
from django.contrib import messages

def login_user(request):
    if request.method=='POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('trade_augur:home_page')
        else:
            messages.add_message(request, messages.INFO, "if you Done have an account press link below to create one")
            return render(request,'login.html',{'form':form})
    else:
        form=AuthenticationForm()
        return render(request,'login.html',{'form':form})

def create_user(request):
    if request.method=='POST':
        form=CustomUserCreationForm(request.POST)
        if form.is_valid:
            form.save()
            return HttpResponse('Thanks ya sokaraaaa')
    else:
        form=CustomUserCreationForm()
        return render(request,'Create_user.html',{'form':form})
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('accounts:login')
    else:
        return HttpResponse('User Not autenticated')


