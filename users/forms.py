from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import TherapistProfile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class TherapistProfileForm(forms.ModelForm):
    class Meta:
        model = TherapistProfile
        fields = ["speciality", "bio", "availability","location"]