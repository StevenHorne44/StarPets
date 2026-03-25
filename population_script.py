import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'starpets_project.settings')
import json
import django

django.setup()

from django.contrib.auth.models import User 
from pets.models import PetType, Pet, PetRating, UserProfile, Bookmark
from django.db.models.signals import post_delete, pre_save
from pets.signals import update_pet_average_rating, auto_delete_pet_file_on_delete
import shutil

def populate():

    #disconnect temporarily to stop errors during clean
    #(this was because PerRating.objects.all().detlete() was triggering the 
    #update_pet_average_rating which called pet.save(), which then tried to open
    #an image file that didnt exist yet.)
    post_delete.disconnect(receiver=update_pet_average_rating, sender=PetRating)

    #Make files for when someone first populates website / to store pet uploads / pfp uploads
    os.makedirs("media/pet_images", exist_ok=True) # Stores current users pets
    os.makedirs("media/profile_pictures", exist_ok=True) # Stores current users pfp
   
    print("Cleaning database...")
    PetRating.objects.all().delete()
    Bookmark.objects.all().delete()
    UserProfile.objects.all().delete()
    Pet.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()
    PetType.objects.all().delete()

    pet_dict = {}
    petPopulationFolder = "population_pets"
    profilePopulationFolder = "population_pfp"
    
    # Copy images from population folder to media folder
    if os.path.exists(petPopulationFolder):
        for filename in os.listdir(petPopulationFolder):
            shutil.copy(f"population_pets/{filename}", f"media/pet_images/{filename}")

    if os.path.exists(profilePopulationFolder):
        for filename in os.listdir(profilePopulationFolder):
            shutil.copy(f"population_pfp/{filename}", f"media/profile_pictures/{filename}")

    with open("pet_types.json") as f:
        pet_types = json.load(f)

    type_objects = {name: add_pet_type(name) for name in pet_types}
   
    user1 = add_user("Steven", "steven@example.com", "12345678f", "Steven.jpg", "Dog and fish owner")
    user2 = add_user("Alexander", "alexander@example.com", "123456789f", "Alexander.jpg", "Big pet lover")
    user3 = add_user("Bob", "bob@example.com", "12345678f", "Bob.jpg", "Pet admirer")
    user4 = add_user("Marjorie", "marjorie@example.com", "12345678f", "Marjorie.png", "I love pets")
    user5 = add_user("Abigail", "abi@example.com", "12345678f", "abi.jpg" ,"EH BELLO")

    # Manually defined pets with correct types
    buddy = add_pet(type_objects['Dog'],   user1, "Buddy",   "A happy german shepherd", 4, "pet_images/Buddy.jpg")
    fluffy = add_pet(type_objects['Cat'],   user2, "Fluffy",  "A fluffy grey cat.",          4, "pet_images/Fluffy.jpg")
    nemo = add_pet(type_objects['Fish'],  user1, "Nemo",    "A bright orange clownfish.",   3, "pet_images/Nemo.jpg")
    bunny = add_pet(type_objects['Rabbit'], user3, "Bunny",   "A soft brown rabbit.",         2, "pet_images/Bunny.jpg")
    gold = add_pet(type_objects['Dog'],   user2, "Gold",    "A friendly golden retriever.", 3, "pet_images/Gold.jpg")
    skittles = add_pet(type_objects['Parrot'],   user4, "Skittles","A colourful playful parrot.",       5, "pet_images/Skittles.jpg")
    noodle = add_pet(type_objects['Snake'],   user3, "Noodle",  "A long snake.",            4, "pet_images/Noodle.jpg")
    speedy = add_pet(type_objects['Turtle'],   user4, "Speedy",  "A slow cheerful turtle.",              3, "pet_images/Speedy.jpg")
    alfie = add_pet(type_objects['Cat'], user2, "Alfie", "A strange and sassy black cat.", 5, "pet_images/Alfie.jpg")
    mack = add_pet(type_objects['Dog'],user4, "Mack", "An angry westie.", 5, "pet_images/Mack.jpg")
    blue = add_pet(type_objects['Dog'], user5, "Blue", "Hes not actually blue", 3, "pet_images/Blue.png")
    waffles = add_pet(type_objects['Cat'], user5, "Waffles", "A biscuit making kitty", 4, "pet_images/Waffles.jpg")


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
    add_comment(blue, user2, "Sleepy!")
    add_comment(mack, user1, "How regal!")
    add_comment(waffles, user3, "Great biscuit making!")
    add_comment(alfie, user5, "What a lovely cat!")

    post_delete.connect(receiver = update_pet_average_rating, sender=PetRating)

    print("Database population complete.")



def add_user(username, email, password, photo_filename, bio):
    user, created = User.objects.get_or_create(username=username, email=email)
    if created:
        user.set_password(password)
        user.save()
        profile = UserProfile.objects.get_or_create(user=user)[0]
        profile.profile_picture = f"profile_pictures/{photo_filename}"
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

    PetRating.objects.get_or_create(PetID=pet, UserID=user, defaults={'stars': stars})
    return pet

def add_comment(pet, user, content):
    rating, created = PetRating.objects.get_or_create(
        PetID=pet,
        UserID=user,
        defaults={'stars': 0}) #acts as "no rating"

    if rating:
        rating.comment = content
        rating.save()
    
    

if __name__ == '__main__':
    print("Starting StarPets population script...")
    populate()
