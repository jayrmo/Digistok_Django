
from django.urls import path
from .views import * #importa todas as funções de dentro do arquivo views

urlpatterns = [
    # path('', homepage, name='homepage'),#cria o link da página homepage(q é def em views).O name é um identificador q aponta para esse caminho dentro da ''.Nesse caso o caminho é o dominio puro..
]
