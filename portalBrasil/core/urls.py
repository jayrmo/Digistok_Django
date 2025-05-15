
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.urls import path
from .views import * 

urlpatterns = [
    # Páginas de Home
    path('', HomePage.as_view(), name='homepage'),
    path('home/', HomeAdmView.as_view(), name='home_adm'),
    
    # CRUD
    path('noticia_form', Noticia_form.as_view(), name='noticia_form'),
    path('nova-noticia/', NoticiaCreateView.as_view(), name='nova-noticia'),
    path('noticia/delete/<int:pk>/', NoticiaDeleteView.as_view(), name='noticia_delete'),
    path('noticia/<int:pk>/editar/', NoticiaUpdateView.as_view(), name='noticia_editar'),

    
    # Login/Logout
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

]
