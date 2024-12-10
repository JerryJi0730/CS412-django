from django import forms
from .models import House,Comment,Buyer

class CreateHouseForm(forms.ModelForm):

    class Meta:
        '''associate this form witht the Comment model'''
        model = House
        # fields = ['article', 'author', 'text', ]
        # remove the article because we want to do this automagically
        fields = ['title','description','price','location','picture','seller']

class CreateBuyerForm(forms.ModelForm):

    class Meta:
        '''associate this form witht the Comment model'''
        model = Buyer
        # fields = ['article', 'author', 'text', ]
        # remove the article because we want to do this automagically
        fields = ['first_name','last_name','email','phone','description','photo']

class UpdateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # Exclude first_name and last_name from being updated
        fields = ['content']