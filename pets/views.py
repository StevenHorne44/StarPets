from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .forms import ExtendedUserCreationForm, UploadForm, UserProfileForm, CustomAuthenticationForm
from .models import Bookmark, Pet, PetType, PetRating, UserProfile, Comment
import datetime
import json

def home(request):
    pets = Pet.objects.all()
    if request.user.is_authenticated:
        for pet in pets:
            pet.user_commented = Comment.objects.filter(
                PetID=pet, 
                UserID=request.user
            ).exists()
    else:
        for pet in pets:
            pet.user_commented = False
    
    return render(request, 'pets/home.html', {'pets': pets})

@login_required
def top_pets(request):
    # Calculate the exact time 7 days ago
    one_week_ago = timezone.now() - datetime.timedelta(days=7)
    
    # Fetch and filter pets added in the last 7 days, then get the top 4 pets based on their average rating, ordered from highest to lowest
    top_pets_list = Pet.objects.filter(date_added__gte=one_week_ago).order_by('-average_rating')[:4]
    
    # If the list is empty, fallback to the all-time top 4
    if not top_pets_list.exists():
        top_pets_list = Pet.objects.order_by('-average_rating')[:4]
    
    # Add comment information for each pet
    for pet in top_pets_list:
        pet.user_commented = Comment.objects.filter(
            PetID=pet, 
            UserID=request.user
        ).exists()
    
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
    
    # Add comment information for each pet
    for pet in pets:
        pet.user_commented = Comment.objects.filter(
            PetID=pet, 
            UserID=request.user
        ).exists()

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
    
    # Add comment information for each bookmarked pet
    for pet in bookmarked_pets:
        pet.user_commented = Comment.objects.filter(
            PetID=pet, 
            UserID=request.user
        ).exists()
    
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

# comments
@login_required
def add_comment(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    
    if Comment.objects.filter(PetID=pet, UserID=request.user).exists():
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'You have already commented on this pet'}, status=400)
        messages.error(request, 'You have already commented on this pet.')
        return redirect('pets:home')
    
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body)
                content = data.get('content', '')
            except:
                content = request.POST.get('content', '')
        else:
            content = request.POST.get('content', '')
        
        if not content or len(content.strip()) == 0:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Comment cannot be empty'}, status=400)
            messages.error(request, 'Comment cannot be empty.')
            return redirect('pets:home')
        
        if len(content) > 200:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Comment is too long (max 200 characters)'}, status=400)
            messages.error(request, 'Comment is too long (max 200 characters).')
            return redirect('pets:home')
        
        comment = Comment(
            PetID=pet,
            UserID=request.user,
            content=content.strip()
        )
        comment.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'comment': {
                    'id': comment.id,
                    'content': comment.content,
                    'username': request.user.username,
                    'created_at': comment.created_at.strftime('%B %d, %Y'),
                    'is_owner': True
                }
            })
        
        messages.success(request, 'Your comment has been posted!')
        return redirect('pets:home')
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def get_comments(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    comments = pet.comments.all() 
    
    user_commented = Comment.objects.filter(
        PetID=pet, 
        UserID=request.user
    ).exists()
    
    comments_data = []
    for comment in comments:
        comments_data.append({
            'id': comment.id,
            'username': comment.UserID.username,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%B %d, %Y'),
            'is_owner': comment.UserID == request.user
        })
    
    return JsonResponse({
        'comments': comments_data,
        'user_commented': user_commented,
        'comments_count': len(comments_data)
    })

@login_required
def delete_comment(request, comment_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.UserID != request.user:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'You can only delete your own comments'}, status=403)
        messages.error(request, 'You can only delete your own comments.')
        return redirect('pets:home')
    
    pet_id = comment.PetID.id
    comment.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Comment deleted successfully',
            'pet_id': pet_id
        })
    
    messages.success(request, 'Your comment has been deleted.')
    return redirect('pets:home')

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.UserID != request.user:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'You can only edit your own comments'}, status=403)
        messages.error(request, 'You can only edit your own comments.')
        return redirect('pets:home')
    
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body)
                new_content = data.get('content', '')
            except:
                new_content = request.POST.get('content', '')
        else:
            new_content = request.POST.get('content', '')
        
        if not new_content or len(new_content.strip()) == 0:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Comment cannot be empty'}, status=400)
            messages.error(request, 'Comment cannot be empty.')
            return redirect('pets:home')
        
        if len(new_content) > 500:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Comment is too long (max 500 characters)'}, status=400)
            messages.error(request, 'Comment is too long (max 500 characters).')
            return redirect('pets:home')
        
        comment.content = new_content.strip()
        comment.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'comment': {
                    'id': comment.id,
                    'content': comment.content,
                    'username': request.user.username,
                    'created_at': comment.created_at.strftime('%B %d, %Y'),
                    'updated_at': comment.updated_at.strftime('%B %d, %Y'),
                    'is_owner': True
                }
            })
        
        messages.success(request, 'Your comment has been updated.')
        return redirect('pets:home')
    
    return JsonResponse({
        'id': comment.id,
        'content': comment.content
    })