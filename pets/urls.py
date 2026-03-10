from django.urls import path
from django.contrib.auth import views as auth_views
from pets import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'pets'

urlpatterns = [
    # name='home' allows you to link to this page easily in your HTML
    path('', views.home, name='home'),
    path('signup', views.sign_up, name='signup'),
    path('login', auth_views.LoginView.as_view(template_name='pets/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
    path('rated/', views.top_pets, name='top_pets'),
    path('categories/', views.categories, name='categories'),
    path('bookmark/', views.bookmarks, name='bookmarks'),
    path('upload/', views.upload_pets, name='upload'),
    path('profile/',views.profile, name='profile'),
    path('toggle-bookmark/<int:pet_id>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('rate-pet/<int:pet_id>/', views.rate_pet, name='rate_pet'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)