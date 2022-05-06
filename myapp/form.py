from django import forms
from .models import Article,Author,Comment,Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class createForm(forms.ModelForm):
    class Meta:
        model=Article
        fields=[
            'title',
            'body',
            'image',
            'category'
        ]
class registerUser(UserCreationForm):
    class Meta:
        model=User
        fields=[
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2'


        ]

class createAuthor(forms.ModelForm):
    class Meta:
        model=Author
        fields= [
            'profile_picture',
            'details',
        ]

class categoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=[
            'name'
        ]

class commnetFrom(forms.ModelForm):
    class Meta:
        model=Comment
        fields= [
            'post_comment'

        ]



class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        labels = {'email':'Email'}
        widget = {'username':forms.TextInput(attrs={'class':'form-control'})}