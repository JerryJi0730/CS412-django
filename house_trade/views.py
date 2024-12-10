from django.shortcuts import render
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin ## NEW
from house_trade.models import House,Seller,Buyer,Comment
from . forms import *
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.urls import reverse ## NEW
from django.contrib.auth import login ## NEW
from django.shortcuts import get_object_or_404, redirect, render
# Create your views here.
class ShowAllHousesView(ListView):
    '''Create a subclass of ListView to display all blog articles.'''
    model = House # retrieve objects of type Article from the database
    template_name = 'house_trade/show_all_houses.html'
    context_object_name = 'houses' # how to find the data in the template file
    def dispatch(self, *args, **kwargs):
        '''
        implement this method to add some tracing
        '''
        print(f"self.request.user={self.request.user}")
        # delegate to superclass version
        return super().dispatch(*args, **kwargs)
    
class ShowAllBuyersView(ListView):
    '''Create a subclass of ListView to display all blog articles.'''
    model = Buyer # retrieve objects of type Article from the database
    template_name = 'house_trade/show_all_buyers.html'
    context_object_name = 'buyers' # how to find the data in the template file
    def dispatch(self, *args, **kwargs):
        '''
        implement this method to add some tracing
        '''
        print(f"self.request.user={self.request.user}")
        # delegate to superclass version
        return super().dispatch(*args, **kwargs)
    
class CreateHouseView(LoginRequiredMixin,CreateView):
    '''a view to show/process the create profile form:
    on GET: sends back the form
    on POST: read the form data, create an instance of Comment; save to database; ??
    '''

    form_class = CreateHouseForm
    template_name = "house_trade/create_house_form.html"
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    
    def form_valid(self, form):
        # find which user is logged in
        user = self.request.user
        print(f'CreateArticleView:form_valid() user={user}')
        # attach the user  to the new article instance
        form.instance.user = user
        # delegate work to superclass
        return super().form_valid(form)
    
    
class ShowSellerPageView(DetailView):
    """
    View to display details of a Seller.

    Attributes:
        model: Specifies the Seller model to retrieve the data.
        template_name: The template used to render the page ('house_trade/seller.html').
        context_object_name: The name of the context variable to use in the template ('seller').
    """
    model = Seller
    template_name = 'house_trade/seller.html'
    context_object_name = 'seller'


class ShowBuyerPageView(DetailView):
    """
    View to display details of a Buyer.

    Attributes:
        model: Specifies the Buyer model to retrieve the data.
        template_name: The template used to render the page ('house_trade/buyer.html').
        context_object_name: The name of the context variable to use in the template ('buyer').
    """
    model = Buyer
    template_name = 'house_trade/buyer.html'
    context_object_name = 'buyer'

def house_detail_view(request, house_id):
    house = get_object_or_404(House, id=house_id)
    return render(request, 'house_trade/comments.html', {'house': house})

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
    
class UpdateCommentView(UpdateView):
    model = Comment
    form_class = UpdateCommentForm
    template_name = 'house_trade/update_comments_form.html'  # Template for the update form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True  # Add a context variable if needed for conditional rendering
        return context
    
    def get_success_url(self):
        # Redirect to the profile page for the user who created this status message
        return reverse('house_comments', kwargs={'house_id': self.object.house.pk})
    
class DeleteCommentsView(DeleteView):
    model = Comment
    template_name = 'house_trade/delete_comments_form.html'
    context_object_name = 'Comment'

    def get_success_url(self):
        # Redirect to the profile page for the user who created this status message
        return reverse('house_comments', kwargs={'house_id': self.object.house.pk})
    