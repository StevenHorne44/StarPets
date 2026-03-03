from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

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
    