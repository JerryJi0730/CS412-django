from django.urls import path
from .views import ShowAllHousesView ,CreateHouseView,ShowSellerPageView,ShowAllBuyersView,ShowBuyerPageView,UpdateCommentView,DeleteCommentsView,CreateBuyerView# our view class definition 
from . import views
from django.contrib.auth import views as auth_views ## NEW
urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllHousesView.as_view(), name='show_all_houses'), # generic class-based view
     path('show_all_buyers', ShowAllBuyersView.as_view(), name='show_all_buyers'), # generic class-based view
    path('create_house', CreateHouseView.as_view(), name="create_house"), ## NEW
    path(r'logout/', auth_views.LogoutView.as_view(next_page='show_all_houses'), 
         name="logout"),
    path('login/', auth_views.LoginView.as_view(template_name='house_trade/login.html'),
           name='login'), ## NEW
     path('seller/<int:pk>', ShowSellerPageView.as_view(), name='seller'),
    path('buyer/<int:pk>', ShowBuyerPageView.as_view(), name='buyer'),
    path('house/<int:pk>', ShowBuyerPageView.as_view(), name='house'),
    path('house/<int:house_id>/comments/', views.house_detail_view, name='house_comments'),
     path('register/', views.RegistrationView.as_view(), name="register"), ## NEW
    path('comments/<int:pk>/update/', UpdateCommentView.as_view(), name='status_update'),
    path('status/<int:pk>/delete/', DeleteCommentsView.as_view(), name='delete_comment'),
    path('create_buyer', CreateBuyerView.as_view(), name="create_buyer"), ## NEW
]