from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models import Avg
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
import os

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
    description = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

#delete old file when a new one is uploaded
@receiver(pre_save, sender=UserProfile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    
    try: 
        old_profile = UserProfile.objects.get(pk=instance.pk)
        old_file = old_profile.profile_picture
    except UserProfile.DoesNotExist:
        return False
    
    new_file = instance.profile_picture

    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

    
#delete file when UserProfile delete (user deletes account)
@receiver(post_delete, sender=UserProfile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.profile_picture:
        if os.path.isfile(instance.profile_picture.path):
            os.remove(instance.profile_picture.path)


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

