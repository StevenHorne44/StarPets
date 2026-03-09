from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .forms import ExtendedUserCreationForm
from .models import Bookmark, Pet, PetType

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

    # Add to the context dictionary the list of pets, types and selected type
    context = {
        'pets': pets,
        'pet_types': pet_types,
        'selected_type': selected_type
    }
    return render(request, 'pets/categories.html', context)

@login_required
def bookmarks(request):
    # Fetch the pets that are bookmarked by the user
    bookmarked_pets = Pet.objects.filter(bookmark__UserID=request.user)
    
    # Add the bookmarked pets to the context dictionary and render the bookmarks template
    context = {
        'pets': bookmarked_pets
    }
    return render(request, 'pets/bookmarks.html', context)

# Backend view for handling bookmark toggling via javascript fetch API
@login_required
def toggle_bookmark(request, pet_id):
    if request.method == 'POST':
        # Fetch the pet based on provided ID or return 404 if not found
        pet = get_object_or_404(Pet, id=pet_id)

        # Get a bookmark or create one if it doesn't exist, then toggle its existence
        bookmark, created = Bookmark.objects.get_or_create(UserID=request.user, PetID=pet)

        if not created:
            # If it already exists, it means we want to remove the bookmark, so we delete it
            bookmark.delete()
            return JsonResponse({'is_bookmarked': False})
        else:
            # If it was created, it means we want to add the bookmark, so we return a success response
            return JsonResponse({'is_bookmarked': True})
        
    # If the request method is not POST, we return an error response indicating an invalid request
    return JsonResponse({'error': 'Invalid request'}, status=400)

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
