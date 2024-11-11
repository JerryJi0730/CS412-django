from django.urls import path
from .views import ShowAllProfilesView # our view class definition 
from .views import ShowProfilePageView,UpdateProfileView,DeleteStatusMessageView,UpdateStatusMessageView,CreateFriendView,ShowFriendSuggestionsView,ShowNewsFeedView
from . import views
from django.contrib.auth import views as auth_views ## NEW
urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'), # generic class-based view
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile', views.CreateProfileView.as_view(), name="create_profile"), ## NEW
     path('profile/create_status', views.CreateStatusMessageView.as_view(), name="create_status"),
     path('profile/update', UpdateProfileView.as_view(), name='update_profile'),
     path('status/<int:pk>/delete/', DeleteStatusMessageView.as_view(), name='delete_status'),
     path('status/<int:pk>/update/', UpdateStatusMessageView.as_view(), name='status_update'),
      path('profile/add_friend/<int:other_pk>/', CreateFriendView.as_view(), name='add_friend'),
    path('profile/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
     path('profile/news_feed/', ShowNewsFeedView.as_view(), name='news_feed'),
      path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'),
           name='login'), ## NEW
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logout.html'), 
         name='logout'), ## NEW
    path('register/', views.RegistrationView.as_view(), name="register"), ## NEW
]