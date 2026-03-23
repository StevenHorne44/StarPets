import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'starpets_project.settings')
import json
import django
django.setup()
from django.contrib.auth.models import User 
from pets.models import PetType, Pet, PetRating, UserProfile, Comment
import shutil

def populate():
    #Make files for when someone first populates website
    os.makedirs("media/PetPhotos", exist_ok=True) # Stores population_script pets
    os.makedirs("media/UserPhotos", exist_ok=True) # Stores population_script user pfp
    os.makedirs("media/pet_images", exist_ok=True) # Stores current users pets
    os.makedirs("media/profile_pictures", exist_ok=True) # Stores current users pfp
   
    PetRating.objects.all().delete()
    Pet.objects.all().delete()
    PetType.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()

    pet_dict = {}
    photoFolder = "population_pets"

    for filename in os.listdir(photoFolder):
        if filename.lower().endswith((".jpg",".png",".jpeg")):
            file_key = os.path.splitext(filename)[0]
            db_path = f"PetPhotos/{filename}"
            pet_dict[file_key] = db_path
    
    # Copy images from PetPhotos to media/PetPhotos
    for filename in os.listdir("population_pets"):
        shutil.copy(f"population_pets/{filename}", f"media/PetPhotos/{filename}")

    for filename in os.listdir("population_users"):
        shutil.copy(f"population_users/{filename}", f"media/UserPhotos/{filename}")

    for name,path in pet_dict.items():
        print(name,"",path)

    with open('pet_types.json') as f:
        pet_types = json.load(f)

    type_objects = {name: add_pet_type(name) for name in pet_types}
    dog_type = type_objects.get('Dog')
    cat_type = type_objects.get('Cat')
    fish_type = type_objects.get('Fish')
    rabbit_type = type_objects.get('Rabbit')
    snake_type = type_objects.get("Snake")
    turtle_type = type_objects.get("Turtle")
    parrot_type = type_objects.get("Parrot")

    user1 = add_user("Steven", "steven@example.com", "12345678f", "Steven.jpg", "Dog and fish owner")
    user2 = add_user("Alexander", "alexander@example.com", "123456789f", "Alexander.jpg", "Big pet lover")
    user3 = add_user("Bob", "bob@example.com", "12345678f", "Bob.jpg", "Pet admirer")
    user4 = add_user("Marjorie", "marjorie@example.com", "12345678f", "Marjorie.png", "I love pets")

    # Manually defined pets with correct types
    buddy = add_pet(dog_type,   user1, "Buddy",   "A happy german shepherd", 5, "PetPhotos/Buddy.jpg")
    fluffy = add_pet(cat_type,   user2, "Fluffy",  "A fluffy grey cat.",          4, "PetPhotos/Fluffy.jpg")
    nemo = add_pet(fish_type,  user1, "Nemo",    "A bright orange clownfish.",   5, "PetPhotos/Nemo.jpg")
    bunny = add_pet(rabbit_type,user3, "Bunny",   "A soft brown rabbit.",         4, "PetPhotos/Bunny.jpg")
    gold = add_pet(dog_type,   user2, "Gold",    "A friendly golden retriever.", 3, "PetPhotos/Gold.jpg")
    skittles = add_pet(parrot_type,   user4, "Skittles","A colourful playful parrot.",       5, "PetPhotos/Skittles.jpg")
    noodle = add_pet(snake_type,   user3, "Noodle",  "A long snake.",            4, "PetPhotos/Noodle.jpg")
    speedy = add_pet(turtle_type,   user4, "Speedy",  "A slow cheerful turtle.",              5, "PetPhotos/Speedy.jpg")

    #Comments
    add_comment(buddy, user2, "What a cute dog!")
    add_comment(buddy, user4, "So cute!")
    add_comment(buddy, user3, "He's so happy!")
    add_comment(fluffy, user1, "Wow!")
    add_comment(skittles, user3, "Colourful wow!")
    add_comment(speedy,   user1, "Love the ironic name!")
    add_comment(speedy,   user2, "Turtles are cool")
    add_comment(noodle, user2, "Brilliant name")
    add_comment(gold, user1, "I want one")
    add_comment(bunny, user4, "Adorable")
    add_comment(nemo, user3, "GOOD NAME!")

    print("Database population complete.")

def add_user(username, email, password, photo_filename, bio):
    user, created = User.objects.get_or_create(username=username, email=email)
    if created:
        user.set_password(password)
        user.save()
        profile = UserProfile.objects.get_or_create(user=user)[0]
        profile.profile_picture = f"UserPhotos/{photo_filename}"
        profile.description = bio
        profile.save()
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

def add_comment(pet, user, content):
    comment, created = Comment.objects.get_or_create(PetID=pet, UserID=user)
    comment.content = content
    comment.save()
    return comment


if __name__ == '__main__':
    print("Starting StarPets population script...")
    populate()
