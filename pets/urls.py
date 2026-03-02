from django.urls import path
from pets import views

app_name = 'pets'

urlpatterns = [
    # name='home' allows you to link to this page easily in your HTML
    path('', views.home, name='home'),
]