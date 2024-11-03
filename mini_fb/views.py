from typing import Any
from django.shortcuts import get_object_or_404, redirect, render
from .models import Profile,Friend
from django.views.generic import ListView
from django.views.generic import DetailView,View
from django.views.generic import CreateView,UpdateView,DeleteView
from . forms import *
from django.urls import reverse ## NEW
from django.contrib.auth.mixins import LoginRequiredMixin ## NEW
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login ## NEW
class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all blog articles.'''
    model = Profile # retrieve objects of type Article from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # how to find the data in the template file
    def dispatch(self, *args, **kwargs):
        '''
        implement this method to add some tracing
        '''
        print(f"self.request.user={self.request.user}")
        # delegate to superclass version
        return super().dispatch(*args, **kwargs)

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'


class CreateProfileView(LoginRequiredMixin,CreateView):
    '''a view to show/process the create profile form:
    on GET: sends back the form
    on POST: read the form data, create an instance of Comment; save to database; ??
    '''

    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    
    def form_valid(self, form):
        print(f'CreateArticleView.form_valid: form.cleaned_data={form.cleaned_data}')

        # find which user is logged in
        user = self.request.user
        print(f'CreateArticleView:form_valid() user={user}')
        # attach the user  to the new article instance
        form.instance.user = user
        # delegate work to superclass
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context
    
class CreateStatusMessageView(LoginRequiredMixin,CreateView):
    '''a view to show/process the create profile form:
    on GET: sends back the form
    on POST: read the form data, create an instance of Comment; save to database; ??
    '''

    form_class = CreateStatusForm
    template_name = "mini_fb/create_status_form.html"
    def get_object(self):
        # Fetch the profile based on the logged-in user
        return Profile.objects.get(user=self.request.user)

    def get_success_url(self) -> str:
        '''return the URL to redirect to after sucessful create'''
        #return "/blog/show_all"
        #return reverse("show_all")
        pk=self.get_object().pk
        return reverse("show_profile", kwargs={'pk': pk})

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''
        build the template context data --
        a dict of key-value pairs.'''

        # get the super class version of context data
        context = super().get_context_data(**kwargs)

        # find the article with the PK from the URL
        # self.kwargs['pk'] is finding the article PK from the URL
        profile = self.get_object()

        # add the article to the context data
        context['article'] = profile

        return context
    

    
    def form_valid(self, form):
        '''this method executes after form submission'''

        print(f'CreateCommentView.form_valid(): form={form.cleaned_data}')
        print(f'CreateCommentView.form_valid(): self.kwargs={self.kwargs}')

        # find the article with the PK from the URL
        # self.kwargs['pk'] is finding the article PK from the URL
        profile = self.get_object()

        # attach the article to the new Comment 
        # (form.instance is the new Comment object)
        form.instance.profile= profile
        sm = form.save()
        files = self.request.FILES.getlist('files')
        for file in files:
            image = Image(image_file=file, status_message=sm)
            image.save()
        # delegaute work to the superclass version of this method
        return super().form_valid(form)
    
class UpdateProfileView(LoginRequiredMixin,UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    
    def get_object(self):
        # Fetch the profile based on the logged-in user
        return Profile.objects.get(user=self.request.user)
    # This function will redirect the user to the profile page after a successful update
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'StatusMessage'

    def get_success_url(self):
        # Redirect to the profile page for the user who created this status message
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'  # Template for the update form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True  # Add a context variable if needed for conditional rendering
        return context
    
    def get_success_url(self):
        # Redirect to the profile page for the user who created this status message
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
class CreateFriendView(LoginRequiredMixin,View):
    """View to handle adding friends."""
    # model=Friend

    def get_object(self):
        # Fetch the profile based on the logged-in user
        return Profile.objects.get(user=self.request.user)
    def dispatch(self, request, *args, **kwargs):
        pk = self.get_object().pk  # Profile doing the adding
        other_pk = self.kwargs['other_pk']  # Profile to be added

        # Fetch the profiles from the database
        profile = get_object_or_404(Profile, pk=pk)
        other_profile = get_object_or_404(Profile, pk=other_pk)

        # Use the add_friend method to add the friend relationship
        profile.add_friend(other_profile)

        # Redirect back to the profile page after adding the friend
        return redirect('show_profile', pk=pk)
    
class ShowFriendSuggestionsView(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    def get_object(self):
        # Fetch the profile based on the logged-in user
        return Profile.objects.get(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['friend_suggestions'] = profile.get_friend_suggestions()
        return context
    
class ShowNewsFeedView(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = 'profile'

    def get_object(self):
        # Fetch the profile based on the logged-in user
        return Profile.objects.get(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        
        # Get the news feed using the get_news_feed method
        context['news_feed'] = profile.get_news_feed()
        
        return context
    
class RegistrationView(CreateView):
    '''Display and process the UserVreationForm for account registration.'''
    template_name = 'mini_fb/register.html'
    form_class = UserCreationForm
    def dispatch(self, *args, **kwargs):
        '''Handle the User creation process.'''
        # we handle the HTTP POST request
        if self.request.POST:
            
            print(f"self.request.POST={self.request.POST}")
            # reconstruct the UserCreationForm from the HTTP POST
            form = UserCreationForm(self.request.POST)
            # print(f'form={form}')
            if not form.is_valid():
                print(f'form.errors={form.errors}')
                # let's the CreateView superclass handle this problem!
                return super().dispatch(*args, **kwargs)
            # save the new User object
            user = form.save() # creates a new instance of User object in the database
            print(f"RegistrationView.dispatch: created user {user}")
            # log in the User
            login(self.request, user)
            print(f"RegistrationView.dispatch, user {user} is logged in.")
            ## mini_fb note: attach user to Profile creation form before saving.
            # redirect the user to some page view...
            return redirect(reverse('create_profile'))
        # let the superclass CreateView handle the HTTP GET request:
        return super().dispatch(*args, **kwargs)