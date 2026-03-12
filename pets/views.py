from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .forms import ExtendedUserCreationForm, UploadForm, UserProfileForm, CustomAuthenticationForm
from .models import Bookmark, Pet, PetType, PetRating, UserProfile
import datetime
import json

# Create your views here.

def home(request):
    return render(request, 'pets/home.html')

@login_required
def top_pets(request):
    # Calculate the exact time 7 days ago
    one_week_ago = timezone.now() - datetime.timedelta(days=7)
    
    # Fetch and filter pets added in the last 7 days, then get the top 4 pets based on their average rating, ordered from highest to lowest
    top_pets_list = Pet.objects.filter(date_added__gte=one_week_ago).order_by('-average_rating')[:4]
    
    # If the list is empty, fallback to the all-time top 4
    if not top_pets_list.exists():
        top_pets_list = Pet.objects.order_by('-average_rating')[:4]
    
    # Add the top pets to the context dictionary and render the top pets template
    context = {
        'top_pets' : top_pets_list
    }
    return render(request, 'pets/top_pets.html', context)

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
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.UserID = request.user
            pet.save()
            return redirect('pets:profile')
    else:
        form = UploadForm()
    return render(request, 'pets/upload.html', {'form':form})

@login_required
def profile(request):
    # get all the pets where UserID == current user
    user_pets = Pet.objects.filter(UserID=request.user) 
    user_profile,created = UserProfile.objects.get_or_create(user=request.user)

    return render(request, 'pets/profile.html', {'pets':user_pets, 'user_profile': user_profile})

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('pets:profile')
    
    return redirect('pets:profile')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been successfully deleted.")
        return redirect('pets:home')
    
    return redirect('pets:profile')

def login_view(request):
    if request.method == 'POST':
        # Pass the request and the POST data to your custom form
        form = CustomAuthenticationForm(request, data=request.POST)
        
        # This is where ReCaptcha is actually verified!
        if form.is_valid(): 
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('pets:home')
    else:
        form = CustomAuthenticationForm()
        
    return render(request, 'pets/login.html', {'form': form})


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

@login_required
def rate_pet(request, pet_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            stars = int(data.get('rating', 0))
            
            if 1<= stars <= 5:
                pet = get_object_or_404(Pet, id=pet_id)
                
                PetRating.objects.update_or_create(
                    UserID=request.user,
                    PetID=pet,
                    defaults={'stars': stars}
                )
                
                pet.refresh_from_db()
                
                return JsonResponse({'success' : True, 'new_average' : pet.average_rating})
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=400)
    return JsonResponse({'error' : 'Invalid request'}, status=400)


#pet deletion
@login_required
def select_pet_delete(request):
    user_pets = Pet.objects.filter(UserID=request.user)
    return render(request, 'pets/select_pet_delete.html', {'pets': user_pets})

@login_required
def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, UserID=request.user)
    if request.method == "POST":
        pet.delete()
        messages.success(request, "Your upload has been successfully deleted.")
        return redirect('pets:home')
    
    return render(request, 'pets/confirm_delete.html', {'pet': pet})

