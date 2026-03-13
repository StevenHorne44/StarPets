from urllib import response
from django.contrib.auth.models import User
from .models import Bookmark, Pet, PetRating, PetType
from django.test import TestCase

# Create your tests here.

# Tests for home page
class HomePageTests(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_correct_content(self):
        response = self.client.get('/')
        self.assertContains(response, 'Welcome to StarPets!')

# Tests for pet model 
class PetModelTests(TestCase):
    # Not a test
    def setUp(self):
        # Create test user and pet
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.dog_type = PetType.objects.create(type_name='Dog')
        self.pet = Pet.objects.create(TypeID=self.dog_type, UserID=self.user, name='Buddy')

    def test_pet_creation(self):
        self.assertEqual(self.pet.name, 'Buddy')
        self.assertEqual(self.pet.TypeID.type_name, 'Dog')
        self.assertEqual(self.pet.UserID.username, 'testuser')           
   
    def test_pet_rating(self):
        # To check rating is dealt with correctly
        rating = PetRating.objects.create(PetID=self.pet, UserID=self.user, stars=5, comment='Great pet!')
        self.assertEqual(rating.stars, 5)
        self.assertEqual(self.pet.name, rating.PetID.name)

    def test_bookmark(self):
        bookmark = Bookmark.objects.create(PetID=self.pet, UserID=self.user)
        self.assertTrue(Bookmark.objects.filter(PetID=self.pet, UserID=self.user).exists())
    
    def test_average_rating_calculation(self):
        self.user2 = User.objects.create_user(username='testuser2', password='password123')
        PetRating.objects.create(PetID=self.pet, UserID=self.user, stars=5)
        PetRating.objects.create(PetID=self.pet, UserID=self.user2, stars=3)
        
        self.pet.refresh_from_db()
        # (5+3)/2 = 4.0
        self.assertEqual(self.pet.average_rating, 4.0)

       