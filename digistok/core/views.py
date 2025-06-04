from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.signals import post_delete, pre_save
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.views.generic import DeleteView
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
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
    
# Cadastra e Lista Fornecedor
class CadastraFornecedor(View):
    def get(self, request):
        busca = request.GET.get('busca')
        status_filtro = request.GET.get('status_filtro', '')
        fornecedores_lista = Fornecedor.objects.all().order_by('id')
        # if busca:
        #     fornecedores_lista = Fornecedor.objects.filter(
        #         Q(cpf_cnpj__icontains=busca) | Q(nome__icontains=busca) | Q(status__iexact=busca)
        #             ).order_by('id')

        if busca and status_filtro:
            fornecedores_lista = Fornecedor.objects.filter(
                (Q(cpf_cnpj__icontains=busca) | Q(nome__icontains=busca)) &
                Q(status__iexact=status_filtro)
            ).order_by('id')
        elif busca:
            fornecedores_lista = Fornecedor.objects.filter(Q(cpf_cnpj__icontains=busca) | Q(nome__icontains=busca)).order_by('id')
        elif status_filtro:
            fornecedores_lista = Fornecedor.objects.filter(status__iexact=status_filtro).order_by('id')
        else:
            fornecedores_lista = Fornecedor.objects.all().order_by('id')    
        
        paginator = Paginator(fornecedores_lista, 5)
        page_number = request.GET.get('page', 1)
        fornecedores = paginator.get_page(page_number)
        
        context = {
            'fornecedores': fornecedores,
            'title': 'Fornecedor',
            'busca': busca
        }
        return render(request, 'digistok/cadastra_fornecedor.html', context)

    def post(self, request):
        cpf_cnpj = request.POST.get('fornecedorCPFCNPJ', '').strip()
        nome = request.POST.get('fornecedorNome', '').strip()
        contato = request.POST.get('fornecedorContato', '').strip()
        endereco = request.POST.get('fornecedorEndereco', '').strip()
        cidade = request.POST.get('fornecedorCidade', '').strip()
        if cpf_cnpj:
            existe = Fornecedor.objects.filter(cpf_cnpj=cpf_cnpj).exists()
        if existe:
            messages.error(request, f'O CPF/CNPJ "{cpf_cnpj}" já está cadastrado.')
            return redirect('cadastra_fornecedor')

        if nome:
            Fornecedor.objects.create(
                cpf_cnpj=cpf_cnpj,
                nome=nome,
                contato=contato,
                endereco=endereco,
                cidade=cidade
                
            )
            messages.success(request, f'Fornecedor "{nome}" cadastrado com sucesso!')
        else:
            messages.error(request, "O nome do fornecedor não pode estar em branco.")

        return redirect('cadastra_fornecedor')


# Edita Fornecedor
class EditaFornecedor(View):
    template_name = 'digistok/cadastra_fornecedor.html'

    def get(self, request, pk):
        fornecedor = get_object_or_404(Fornecedor, pk=pk)
        fornecedores = Fornecedor.objects.all()
        return render(request, self.template_name, {
            'fornecedor': fornecedor,
            'fornecedores': fornecedores,
            'status_ativo': fornecedor.status == 'Ativo'
        })

    def post(self, request, pk):
        fornecedor = get_object_or_404(Fornecedor, pk=pk)
        fornecedor.nome = request.POST.get('fornecedorNome', '').strip()
        fornecedor.contato = request.POST.get('fornecedorContato', '').strip()
        fornecedor.endereco = request.POST.get('fornecedorEndereco', '').strip()
        fornecedor.cidade = request.POST.get('fornecedorCidade', '').strip()
        status = 'Ativo' if request.POST.get('fornecedorStatus') == 'Ativo' else 'Inativo'
        fornecedor.status = status
        fornecedor.save()
        messages.success(request, "Fornecedor atualizado com sucesso!")
        return redirect('cadastra_fornecedor')


# Apaga Fornecedor individual
class ApagaFornecedor(DeleteView):
    model = Fornecedor
    template_name = 'digistok/cadastra_fornecedor.html'
    success_url = reverse_lazy('cadastra_fornecedor')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        nome_fornecedor = self.object.nome
        self.object.delete()
        messages.success(request, f'Fornecedor "{nome_fornecedor}" apagado com sucesso.')
        return HttpResponseRedirect(self.success_url)


# Apaga múltiplos fornecedores
@method_decorator(csrf_exempt, name='dispatch')
class ApagaFornecedoresSelecionados(View):
    def post(self, request):
        ids = request.POST.getlist('fornecedores_selecionados')
        if ids:
            fornecedores = Fornecedor.objects.filter(id__in=ids)
            quantidade = fornecedores.count()
            nome_primeiro = fornecedores[0].nome if quantidade == 1 else None
            fornecedores.delete()
            if quantidade == 1:
                messages.success(request, f'Fornecedor "{nome_primeiro}" apagado com sucesso.')
            else:
                messages.success(request, f'"{quantidade}" fornecedores apagados com sucesso.')
        else:
            messages.warning(request, "Nenhum fornecedor selecionado para exclusão.")
        return redirect('cadastra_fornecedor')


# CRUD CATEGORIA--------------------------------------
# Cadastra e Lista Categoria 
class CadastraCategoria(View):
    def get(self, request):
        categorias_lista = Categoria.objects.all().order_by('id')
        busca = request.GET.get('busca')

        if busca:
            categorias_lista = Categoria.objects.filter(nome__icontains=busca).order_by('id')
        else:
            categorias_lista = Categoria.objects.all().order_by('id')
        paginator = Paginator(categorias_lista, 5)
        page_number = request.GET.get('page', 1)
        categorias = paginator.get_page(page_number)
        
        context = {
            'categorias': categorias,
            'title': 'Categoria',
            'busca': busca
        }
        return render (request, 'digistok/cadastra_categoria.html', context)
    
    def post(self, request):
        nome = request.POST.get('categoriaNome', '').strip()
        if nome:
            existe = Categoria.objects.filter(nome=nome).exists()
        if existe:
            messages.error(request, f'A categoria "{nome}" já está cadastrada.')
            return redirect('cadastra_categoria')
        if nome:
            Categoria.objects.create(nome = nome)
            messages.success(self.request, f'Categoria "{ nome }" salva com sucesso!')
        else:
            messages.error(self.request, "O nome da categoria não pode estar em branco.")
        return redirect('cadastra_categoria')
                     

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
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        nome_categoria = self.object.nome
        self.object.delete()
        messages.success(request, f'Categoria "{nome_categoria}" apagada com sucesso.')
        return HttpResponseRedirect(self.success_url)
    
@method_decorator(csrf_exempt, name='dispatch')
class ApagaCategoriasSelecionadas(View):
    def post(self, request):
        ids = request.POST.getlist('categorias_selecionadas')
        if ids:
            categorias = Categoria.objects.filter(id__in=ids)
            quantidade = categorias.count()
            nome_primeira_categoria = categorias[0].nome if quantidade == 1 else None
            categorias.delete()
            if quantidade == 1 :
                messages.success(request, f'Categoria "{nome_primeira_categoria}" apagada com sucesso.')
            else:            
                messages.success(request, f'"{quantidade}"categorias apagadas com sucesso.')
        else:
            messages.warning(request, "Nenhuma categoria foi selecionada para exclusão.")
        return redirect('cadastra_categoria')    
    

