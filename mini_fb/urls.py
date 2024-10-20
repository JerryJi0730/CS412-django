from django.urls import path
from .views import ShowAllProfilesView # our view class definition 
from .views import ShowProfilePageView,UpdateProfileView,DeleteStatusMessageView,UpdateStatusMessageView
from . import views
urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'), # generic class-based view
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile', views.CreateProfileView.as_view(), name="create_profile"), ## NEW
     path('profile/<int:pk>/create_status', views.CreateStatusMessageView.as_view(), name="create_status"),
     path('profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'),
     path('status/<int:pk>/delete/', DeleteStatusMessageView.as_view(), name='delete_status'),
     path('status/<int:pk>/update/', UpdateStatusMessageView.as_view(), name='status_update'),
]