from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
from .forms import ExtendedUserCreationForm
from .models import Pet, PetType

# Create your views here.

def home(request):
    return render(request, 'pets/home.html')

@login_required
def top_pets(request):
    return render(request, 'pets/top_pets.html')

@login_required
def categories(request):
    # Fetch all pet types for the filter
    pet_types = PetType.objects.all()
    selected_type = request.GET.get('type')
    
    # Apply a filter or return ALL pets if no filter is selected
    if selected_type and selected_type != 'all':
        pets = Pet.objects.filter(TypeID__type_name=selected_type)
    else:
        pets = Pet.objects.all()

    # Add to the context dictionary the list of petss, types and selected type
    context = {
        'pets': pets,
        'pet_types': pet_types,
        'selected_type': selected_type
    }
    return render(request, 'pets/categories.html', context)

@login_required
def bookmarks(request):
    return render(request, 'pets/bookmarks.html')

@login_required
def upload_pets(request):
    return render(request, 'pets/upload.html')

@login_required
def profile(request):
    return render(request, 'pets/profile.html')

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
