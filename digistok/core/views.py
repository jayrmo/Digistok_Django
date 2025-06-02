from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.signals import post_delete, pre_save
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from .models import *
import os

# Create your views here.
@method_decorator(never_cache, name='dispatch')
class HomePage(View):
    def get(self, request): 
        # noticias = Noticia.objects.all().order_by('-data_publicacao')     
        context = {
            'title': 'Home',
            # 'noticias': noticias,
        }
        return render(request, 'digistok/homepage.html', context) 
    
    
class CadastraProduto(View):
    def get(self, request):
        context = {
            'title': 'Produto',
        }
        return render (request, 'digistok/cadastra_produto.html', context)
    
class CadastraFornecedor(View):
    def get(self, request):
        context = {
            'title': 'Fornecedor',
        }
        return render (request, 'digistok/cadastra_fornecedor.html', context)
    



# CRUD CATEGORIA--------------------------------------
# Cadastra e Lista Categoria 
class CadastraCategoria(View):
    def get(self, request):
        categorias = Categoria.objects.all()
        context = {
            'categorias': categorias,
            'title': 'Categoria',
        }
        return render (request, 'digistok/cadastra_categoria.html', context)
    
    def post(self, request):
        nome = request.POST.get('categoriaNome', '').strip()
        if nome:
            Categoria.objects.create(nome = nome)
            messages.success(self.request, "Categoria salva com sucesso!")
            return redirect('cadastra_categoria')
        else: 
            return render(request,'digistok/cadastra_categoria.html')
            

# Edita Categoria
class EditaCategoria(View):
    model = Categoria
    template_name = 'digistok/cadastra_categoria.html'

    def get(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        categorias = Categoria.objects.all()
        return render(request, self.template_name,{'categoria': categoria, 'categorias': categorias})

    def post(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        categoria.nome = request.POST.get('categoriaNome')
        categoria.save()
        messages.success(request, "Categoria atualizada com sucesso!")
        return redirect('cadastra_categoria')

#Apagar Categoria
class ApagaCategoria(DeleteView):
    model = Categoria
    template_name = 'digistok/cadastra_categoria.html'
    success_url = reverse_lazy('cadastra_categoria')
    

