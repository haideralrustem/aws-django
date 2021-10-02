from django import forms
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile



class MyUserRegisterForm(UserCreationForm):
    # Django authentication framework provides a form named UserCreationForm (which inherits from ModelForm class) to handle the creation of new users. It has three fields namely username, password1 and password2
    email = forms.EmailField()

    class  Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

#..................

class UserUpdateForm(forms.ModelForm):
    
    class  Meta:
        model = User
        fields = ['username']
        widgets = {
           'username': forms.TextInput(attrs={'placeholder': 'username'}),
        }


#.....................

class UserEmailUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class  Meta:
        model = User
        fields = ['email']


#.................

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']