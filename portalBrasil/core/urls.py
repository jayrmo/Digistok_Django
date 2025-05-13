
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import * 

urlpatterns = [
    # path('noticia/login/', login, name='login'),
    path('login/', LoginView.as_view(),
name='login'),
    path('login/', auth_views.LogoutView.as_view(), name='logout'),


]
