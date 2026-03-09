import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'starpets_project.settings')

import django
django.setup()
from django.contrib.auth.models import User 
from pets.models import PetType, Pet, PetRating
import os

def populate():

    pet_dict = {}
    photoFolder = "media/PetPhotos"

    for filename in os.listdir(photoFolder):
        if filename.lower().endswith((".jpg",".png",".jpeg")):
            file_key = os.path.splitext(filename)[0]
            db_path = f"PetPhotos/{filename}"
            pet_dict[file_key] = db_path
    
    for name,path in pet_dict.items():
        print(name,"",path)

    dog_type = add_pet_type('Dog')
    cat_type = add_pet_type('Cat')
    bird_type = add_pet_type('Bird')

    user1 = add_user("Steven", "steven@example.com","12345678f")
    user2 = add_user("Alexander", "alexander@example.com","123456789f")

    pets = []
    i = 0
    for name,path in pet_dict.items():
        if i % 2 == 0:
            pets.append(add_pet(dog_type, user1, name, "PLACEHOLDER DESC", 5, path))
        else:
            pets.append(add_pet(dog_type,user2,name,"PLACEHOLDER DESC",5,path))
        i+=1

    print("Database population complete.")

def add_user(username, email, password):
    user, created = User.objects.get_or_create(username=username, email=email)
    if created:
        user.set_password(password)
        user.save()
    return user 

def add_pet_type(name):
    pet_type = PetType.objects.get_or_create(type_name=name)[0]
    pet_type.save()
    return pet_type
    
def add_pet(pet_type, user, name, description, stars, photo_path):
    pet = Pet.objects.get_or_create(TypeID=pet_type, UserID=user, name=name)[0]
    pet.description = description
    pet.picture = photo_path
    pet.save()

    PetRating.objects.get_or_create(PetID=pet, UserID=user, stars=stars)
    return pet


if __name__ == '__main__':
    print("Starting StarPets population script...")
    populate()
