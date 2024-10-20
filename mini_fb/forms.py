from django import forms
from .models import Profile, StatusMessage,Image

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

class CreateImage(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['image_file']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # Exclude first_name and last_name from being updated
        fields = ['city', 'email_address', 'profile_image_url']

class UpdateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        # Exclude first_name and last_name from being updated
        fields = ['message']