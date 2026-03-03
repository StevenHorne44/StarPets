import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'starpets_project.settings')

import django
django.setup()
from django.contrib.auth.models import User 
from pets.models import PetType, Pet, PetRating

def populate():

    dog_type = add_pet_type('Dog')
    cat_type = add_pet_type('Cat')
    bird_type = add_pet_type('Bird')

    user1 = add_user("Steven", "steven@example.com")
    user2 = add_user("Alexander", "alexander@example.com")
    
    pet1 = add_pet(dog_type, user1, "Ralph", "A friendly dog", 5)
    pet2 = add_pet(cat_type, user2, "Whiskers", "A playful cat", 3)
    pet3 = add_pet(bird_type, user1, "Tweety", "A cheerful bird", 2)

    print("Database population complete.")

def add_user(username, email):
    user, created = User.objects.get_or_create(username=username, email=email)
    if created:
        user.set_password('password')
        user.save()
    return user 

def add_pet_type(name):
    pet_type = PetType.objects.get_or_create(type_name=name)[0]
    pet_type.save()
    return pet_type
    
def add_pet(pet_type, user, name, description, stars):
    pet = Pet.objects.get_or_create(TypeID=pet_type, UserID=user, name=name)[0]
    pet.description = description
    pet.save()

    PetRating.objects.get_or_create(PetID=pet, UserID=user, stars=stars)
    return pet


if __name__ == '__main__':
    print("Starting StarPets population script...")
    populate()
