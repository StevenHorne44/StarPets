from django.contrib import admin
from pets.models import Bookmark, PetType, Pet, PetRating, UserProfile

admin.site.register(PetType)
admin.site.register(Pet)
admin.site.register(PetRating)  
admin.site.register(Bookmark)
admin.site.register(UserProfile)