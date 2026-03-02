from django.urls import path
from pets import views

app_name = 'pets'

urlpatterns = [
    # name='home' allows you to link to this page easily in your HTML
    path('', views.home, name='home'),
    path('signup', views.register, name='register'),
    path('login', views.login, name='login'),
    path('rated/', views.top_pets, name='top_pets'),
    path('browse/', views.categories, name='categories'),
    path('bookmark/', views.bookmarks, name='bookmarks'),
    path('upload/', views.upload_pets, name='upload'),
]