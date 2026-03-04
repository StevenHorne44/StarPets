from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
from .forms import ExtendedUserCreationForm

# Create your views here.

def home(request):
    return render(request, 'pets/home.html')

#@login_required
def top_pets(request):
    return render(request, 'pets/top_pets.html')

#@login_required
def categories(request):
    return render(request, 'pets/categories.html')

#@login_required
def bookmarks(request):
    return render(request, 'pets/bookmarks.html')

#@login_required
def upload_pets(request):
    return render(request, 'pets/upload.html')

def sign_up(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)
            messages.success(request, f"Welcome to StarPets, {user.username}!")
            return redirect('pets:home')

    else:
        form = ExtendedUserCreationForm()
    return render(request, 'pets/signup.html', {'form':form})
