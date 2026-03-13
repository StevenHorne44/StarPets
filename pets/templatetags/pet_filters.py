from django import template
from django.utils.safestring import mark_safe
from pets.models import Bookmark, PetRating

#registering the template library
register = template.Library()

@register.filter(name='draw_stars')
def draw_stars(stars):
    #try to convert the input to a float, if it fails, default to 0.0
    try:
        stars = float(stars)
    except (ValueError, TypeError):
        stars = 0.0
        
    #ensure stars is between 0.0 and 5.0
    stars = max(0.0, min(stars, 5.0))
    
    # Calculate the width percentage for the gold stars
    fill_percentage = (stars / 5.0) * 100
    
    # Create the overlay HTML
    # Use relative positioning for the wrapper, and absolute positioning for the gold stars
    html = f'''
        <strong style="color: #374151;">Average Rating:</strong> 
        
        <span class="star-rating-wrapper" style="display: inline-block; position: relative; letter-spacing: 2px; font-size: 1.2rem; pointer-events: none;">
            <span style="color: #e5e7eb; display: inline-block;">★★★★★</span>
            <span class="gold-stars-overlay" style="position: absolute; top: 0; left: 0; white-space: nowrap; overflow: hidden; width: {fill_percentage}%; pointer-events: none;">
                <span style="color: #f59e0b;">★★★★★</span>
            </span>
        </span> 
        
        <span class="rating-text" style="color: #6b7280; font-weight: bold; margin-left: 5px;">({stars:.1f}/5.0)</span>
    '''
    
    return mark_safe(html)

@register.simple_tag
def get_user_rating(pet, user):
    if user.is_authenticated:
        rating = PetRating.objects.filter(PetID=pet, UserID=user).first()
        if rating:
            return rating.stars
    return 0

@register.simple_tag
def has_user_bookmarked(pet, user):
    """Returns True if the user has bookmarked this pet, False otherwise."""
    if user.is_authenticated:
        return Bookmark.objects.filter(PetID=pet, UserID=user).exists()
    return False