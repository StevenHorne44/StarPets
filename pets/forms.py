from django import forms
from .models import Pet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Enter your email here")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)


class UploadForm(forms.ModelForm):
    
    name = forms.CharField(required=True, help_text="Enter your pets name below:")
    picture = forms.ImageField(required=True, help_text="Upload an image of your pet here")
    description = forms.CharField(help_text="Describe your pet below:")

    class Meta:
        model = Pet
        exclude = ('UserID', 'average_rating')