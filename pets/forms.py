from django import forms
from .models import Pet, PetType, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Enter your email here")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)


class UploadForm(forms.ModelForm):
    name = forms.CharField(required=True, label="Enter your pets name:")
    TypeID = forms.ModelChoiceField(required=True, queryset=PetType.objects.none(), label="Select pet category:")
    picture = forms.ImageField(required=True, label="Upload pet image")
    description = forms.CharField(label="Description:")

    class Meta:
        model = Pet
        exclude = ('UserID', 'average_rating')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['TypeID'].queryset = PetType.objects.all().order_by('type_name')


class UserProfileForm(forms.ModelForm):
    description = forms.CharField(required=False, max_length=200, help_text="Enter your description here!")
    profile_picture = forms.ImageField(required=False, help_text="Upload a profile picture")

    class Meta:
        model = UserProfile
        fields = ('profile_picture','description')

