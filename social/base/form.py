from django import forms
from .models import Twitter,Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class ProfilePicForms(forms.ModelForm):
    profile_image = forms.ImageField(label="profile pic")
    profile_bio = forms.CharField(label="", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder': 'enter your bio'}))
    
    homepage_link = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'home page link'}))
    instagram_link = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'instagram link'}))
    linkedin_link = forms.CharField(label="",  widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'linkein link'}))
    
    
    class Meta:
        model = Profile
        fields = ['profile_image','profile_bio', 'homepage_link', 'instagram_link', 'linkedin_link']



class TweetForm(forms.ModelForm):
    body = forms.CharField(required=True, widget=forms.widgets.Textarea(
        attrs={
            "placeholder": "enter your tweet",
            "class": 'form-control'
        }
    ), label="",)
    
    class Meta:
        model = Twitter
        exclude = ('user','likes')
        

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'email address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'first name address'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'last name address'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class']= 'form-control'
        self.fields['username'].widget.attrs['placeholder']= 'enter your username'
        self.fields['username'].label = ""
        self.fields['username'].help_text = '<span class="form-text text-mutex"> <small>Required. 150 character or fewer </small> </span>'
        
        self.fields['password1'].widget.attrs['class']= 'form-control'
        self.fields['password1'].widget.attrs['placeholder']= 'enter your password'
        self.fields['password1'].label = ""
        self.fields['password1'].help_text = '<span class="form-text text-mutex"> <small>password is too common use capital letter, symbol and more than 8 charachter</small> </span>'

        
        self.fields['password2'].widget.attrs['class']= 'form-control'
        self.fields['password2'].widget.attrs['placeholder']= 'confirm your password'
        self.fields['password2'].label = ""
        self.fields['password2'].help_text = '<span class="form-text text-mutex"> <small>password does not match </small> </span>'


    