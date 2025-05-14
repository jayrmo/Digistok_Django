
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.urls import path
from .views import * 

urlpatterns = [
    path('', HomePage.as_view(), name='homepage'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
