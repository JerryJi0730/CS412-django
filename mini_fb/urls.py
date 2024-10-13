from django.urls import path
from .views import ShowAllProfilesView # our view class definition 
from .views import ShowProfilePageView
urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'), # generic class-based view
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),
]