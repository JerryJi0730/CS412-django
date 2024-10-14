from django.urls import path
from .views import ShowAllProfilesView # our view class definition 
from .views import ShowProfilePageView
from . import views
urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'), # generic class-based view
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile', views.CreateProfileView.as_view(), name="create_profile"), ## NEW
     path('profile/<int:pk>/create_status', views.CreateStatusMessageView.as_view(), name="create_status")
]