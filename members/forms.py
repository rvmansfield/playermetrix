from django import forms

from django.contrib.auth.models import User
from .models import Profile
from players.models import Players
from django.contrib.auth.forms import UserCreationForm
from django_recaptcha.fields import ReCaptchaField


class UpdateUserForm(forms.ModelForm):
    
    first_name = forms.CharField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name','last_name','email']


class UpdateProfileForm(forms.ModelForm):
    
    location = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['location']

class UpdatePlayerForm(forms.ModelForm):
    
    GRAD_YEAR_CHOICES = ( 
    ("2022", "2022"), 
    ("2023", "2023"), 
    ("2024", "2024"), 
    ("2025", "2025"), 
    ("2026", "2026"), 
    ("2027", "2027"), 
    ("2028", "2028"), 
    ("2029", "2029"), 
    ("2030", "2030"), 
) 
    
    POSITIONS = ( 
    ("P", "Pitcher"), 
    ("C", "Catcher"), 
    ("1B", "First Base"), 
    ("2B", "Second Base"), 
    ("3B", "Third Base"), 
    
) 
    
    THROWS_HITS = ( 
    ("R", "Right"), 
    ("L", "Left"), 
    ("B", "Both"), 
) 

    firstName = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastName = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    highSchool = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    gradYear = forms.IntegerField(required=False, widget=forms.Select(choices=GRAD_YEAR_CHOICES,attrs={'class': 'form-control'}))
    throws = forms.CharField(required=False, widget=forms.Select(choices=THROWS_HITS,attrs={'class': 'form-control'}))
    hits = forms.CharField(required=False, widget=forms.Select(choices=THROWS_HITS,attrs={'class': 'form-control'}))
    instagramUser = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    xUser = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    pitcher = forms.BooleanField(required=False, label='Pitcher', widget=forms.CheckboxInput())
    catcher = forms.BooleanField(required=False, label='Catcher', widget=forms.CheckboxInput())
    firstbase = forms.BooleanField(required=False, label='First Base', widget=forms.CheckboxInput())
    secondbaase = forms.BooleanField(required=False, label='Second Base', widget=forms.CheckboxInput())
    thirdbase = forms.BooleanField(required=False, label='Third Base', widget=forms.CheckboxInput())
    shortstop = forms.BooleanField(required=False, label='Short Stop', widget=forms.CheckboxInput())
    leftfield = forms.BooleanField(required=False, label='Left Field', widget=forms.CheckboxInput())
    centerfield = forms.BooleanField(required=False, label='Center Field', widget=forms.CheckboxInput())
    rightfield = forms.BooleanField(required=False, label='Right Field', widget=forms.CheckboxInput())
    picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    slug = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Players
        fields = ['firstName','lastName','highSchool','gradYear','throws','hits','picture','slug','instagramUser','xUser','pitcher','catcher','firstbase','secondbase','thirdbase','shortstop','leftfield','centerfield','rightfield']



class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    captcha = ReCaptchaField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2','captcha']