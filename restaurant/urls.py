from django.urls import path
from django.conf import settings
# Create your views here.
from . import views
urlpatterns = [
    path(r'', views.main, name="main"), 
    path(r'main', views.main, name="main"), 
    path(r'order', views.order, name="order"), 
    path(r'confirmation', views.confirmation, name="confirmation"), 
    # path(r'submit', views.submit, name="submit"),
    

    

]