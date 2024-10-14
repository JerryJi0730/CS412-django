from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):

    class Meta:
        '''associate this form witht the Comment model'''
        model = Profile
        # fields = ['article', 'author', 'text', ]
        # remove the article because we want to do this automagically
        fields = ['first_name','last_name','city','email_address','profile_image_url',]

class CreateStatusForm(forms.ModelForm):

    class Meta:
        '''associate this form with the Comment model'''
        model = StatusMessage
        fields = ['message']