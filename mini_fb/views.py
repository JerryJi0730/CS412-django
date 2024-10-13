from django.shortcuts import render
from .models import Profile
from django.views.generic import ListView
from django.views.generic import DetailView
class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all blog articles.'''
    model = Profile # retrieve objects of type Article from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # how to find the data in the template file

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'