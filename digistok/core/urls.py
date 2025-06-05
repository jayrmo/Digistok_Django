from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.urls import path, include
from .views import * 

urlpatterns = [
    # Páginas de Home
    path('homepage/', DashboardMovimentacoesView.as_view(), name='homepage'),
    path('relatorio/movimentacoes/', RelatorioMovimentacoesView.as_view(), name='relatorio_movimentacoes'),
    
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
    path('movimentacao-estoque/delete/<int:pk>/', ApagaMovimentacao.as_view(), name='apaga_movimentacao'),
    path('movimentacao-estoque/apagar_selecionados/', ApagaMovimentacoesSelecionadasView.as_view(), name='apaga_movimentacoes_selecionadas'),

    # CRUD LOCAL
    path('cadastra_local', CadastraLocal.as_view(), name='cadastra_local'),
    path('local/<int:pk>/editar/', EditaLocal.as_view(), name='editar_local'),
    path('local/delete/<int:pk>/', ApagaLocal.as_view(), name='apaga_local'),
    path('local/apagar_selecionados/', ApagaLocaisSelecionados.as_view(), name='apaga_locais_selecionados'),

    # Sua URL para alterar a senha com seu formulário customizado
    path('minha-senha/alterar/', PasswordChangeCustomView.as_view(), name='password_change_custom'),

    # URL para a página de sucesso após a alteração
    path('minha-senha/alterar/sucesso/', PasswordChangeDoneCustomView.as_view(), name='password_change_done_custom'),
    

]