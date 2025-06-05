from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.urls import path, include
from .views import * 

urlpatterns = [
    # Páginas de Home
    path('homepage/', HomePage.as_view(), name='homepage'),
    # path('login/', Login.as_view(),name='login'),
    # path('login/', auth_views.LogoutView.as_view(), name='logout'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    # # CRUD PRODUTO
    path('cadastra_produto', CadastraProduto.as_view(), name='cadastra_produto'),
    path('produto/<int:pk>/editar/', EditaProduto.as_view(), name='editar_produto'),
    path('produto/delete/<int:pk>/', ApagaProduto.as_view(), name='apaga_produto'),
    path('produto/apagar_selecionados/', ApagaProdutosSelecionados.as_view(), name='apaga_produtos_selecionados'),
    
    # CRUD Categoria
    path('cadastra_categoria', CadastraCategoria.as_view(), name='cadastra_categoria'),
    path('categoria/<int:pk>/editar/', EditaCategoria.as_view(), name='editar_categoria'),
    path('categoria/delete/<int:pk>/', ApagaCategoria.as_view(), name='apaga_categoria'),
    path('categoria/apagar_selecionados/', ApagaCategoriasSelecionadas.as_view(), name='apaga_selecionadas'),

    # CRUD FORNECEDOR
    path('cadastra_fornecedor', CadastraFornecedor.as_view(), name='cadastra_fornecedor'),
    path('fornecedor/<int:pk>/editar/', EditaFornecedor.as_view(), name='editar_fornecedor'),
    path('fornecedor/delete/<int:pk>/', ApagaFornecedor.as_view(), name='apaga_fornecedor'),
    path('fornecedor/apagar_selecionados/', ApagaFornecedoresSelecionados.as_view(), name='apaga_selecionados'),
    
    # CRUD MOVIMENTAÇÂO
    path('movimentacao-estoque/', MovimentacaoEstoqueView.as_view(), name='movimentacao_estoque'),
    path('movimentacao-estoque/editar/<int:pk>/', MovimentacaoEstoqueView.as_view(), name='editar_movimentacao'),
    path('movimentacao-estoque/excluir-selecionados/', ApagaMovimentacoesSelecionadasView.as_view(), name='apaga_movimentacoes_selecionadas'),
    # .
    # path('noticia_form', Noticia_form.as_view(), name='noticia_form'),
    # path('nova-noticia/', NoticiaCreateView.as_view(), name='nova-noticia'),

    
    # # Login/Logout
    # path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

]