from urllib import response
from django.contrib.auth.models import User
from django.urls import reverse
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

# model testsS
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


# view tests
# tests for top pets view 
class TopPetsViewTests(TestCase):
    
    def setUp(self):
        # create test user
        self.user = User.objects.create_user(username='testuser', password='password123')
    
    # test that user cannot access pages unless logged in
    def test_login_required(self):
        #for top pets access
        response = self.client.get(reverse('pets:top_pets'))
        self.assertEqual(response.status_code, 302)
        #for category access
        response = self.client.get(reverse('pets:categories'))
        self.assertEqual(response.status_code, 302)
        #for bookmarks access
        response = self.client.get(reverse('pets:bookmarks'))
        self.assertEqual(response.status_code, 302)
        #for upload page
        response = self.client.get(reverse('pets:upload'))
        self.assertEqual(response.status_code, 302)

    # test that when no pets, page still loads
    def test_top_pets_empty(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('pets:top_pets'))
        self.assertEqual(response.status_code, 200)

    
        
