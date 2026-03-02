from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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

def register(request):
    return render(request, 'pets/register.html')

def login(request):
    return render(request, 'pets/login.html')