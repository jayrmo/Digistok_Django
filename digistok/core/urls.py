from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.urls import path
from .views import * 

urlpatterns = [
    # Páginas de Home
    path('', HomePage.as_view(), name='homepage'),
    
    # # CRUD
    path('cadastra_produto', CadastraProduto.as_view(), name='cadastra_produto'),
    path('cadastra_fornecedor', CadastraFornecedor.as_view(), name='cadastra_fornecedor'),
    path('cadastra_categoria', CadastraCategoria.as_view(), name='cadastra_categoria'),
    path('categoria/<int:pk>/editar/', EditaCategoria.as_view(), name='editar_categoria'),
    path('categoria/delete/<int:pk>/', ApagaCategoria.as_view(), name='apaga_categoria'),
    # path('noticia_form', Noticia_form.as_view(), name='noticia_form'),
    # path('nova-noticia/', NoticiaCreateView.as_view(), name='nova-noticia'),

    
    # # Login/Logout
    # path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

]