from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.

class PetType(models.Model):
    type_name = models.CharField(max_length=128, unique=True)
    
    class Meta:
        verbose_name_plural = "Pet Types"

    def __str__(self):
        return self.type_name

class Pet(models.Model):
    TypeID = models.ForeignKey(PetType, on_delete=models.CASCADE)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    picture = models.ImageField(upload_to='pet_images', blank=True)
    description = models.TextField(default="No description provided.")
    date_added = models.DateTimeField(auto_now_add=True)
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class PetRating(models.Model):
    PetID = models.ForeignKey(Pet, on_delete=models.CASCADE)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(default=0)
    comment = models.TextField(blank=True, max_length=200)
    rating_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('PetID', 'UserID')

    def __str__(self):
        return f"{self.UserID.username} rated {self.PetID.name} with {self.stars}"

class Bookmark(models.Model):
    PetID = models.ForeignKey(Pet, on_delete=models.CASCADE)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    bookmark_date= models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.UserID.username} bookmarked {self.PetID.name}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)
    

    def __str__(self):
        return self.user.username

# Signal to update average rating of a pet whenever a new rating is added or deleted
@receiver(post_save, sender='pets.PetRating')
@receiver(post_delete, sender='pets.PetRating')
# Listens for any save() or delete() on a PetRating. When triggered recalculates the average and updates the parent Pet.
def update_pet_average_rating(sender, instance, **kwargs):
    pet = instance.PetID
    
    # Calculate the new average for this specific pet
    avg_dict = pet.petrating_set.aggregate(Avg('stars'))
    new_avg = avg_dict['stars__avg']
    
    # If all ratings were deleted, new_avg will be None. Default back to 0.0.
    pet.average_rating = new_avg if new_avg is not None else 0.0
    
    # Save the updated average to the db
    pet.save()