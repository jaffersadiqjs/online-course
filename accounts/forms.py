from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')
