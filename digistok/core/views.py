from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.signals import post_delete, pre_save
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.views.generic import DeleteView
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.http import HttpResponse
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
    
    
  
# INICIO CRUD PRODUTO ----------------------------  
# Cadastra e Lista Produto
class CadastraProduto(View):
    def get(self, request):
        busca = request.GET.get('busca')
        fornecedores = Fornecedor.objects.all().order_by('id')
        categorias = Categoria.objects.all().order_by('id')
        produtos_lista = Produto.objects.all().order_by('id')
        if busca:
            produtos_lista = Produto.objects.filter(
                Q(codigo__icontains=busca) | Q(descricao__icontains=busca) | Q(categoria__nome__iexact=busca)
                    ).order_by('id')
        else:
            produtos_lista = Produto.objects.all().order_by('id')    
        
        paginator = Paginator(produtos_lista, 5)
        page_number = request.GET.get('page', 1)
        produtos = paginator.get_page(page_number)
        
        context = {
            'produtos' : produtos,
            'fornecedores': fornecedores,
            'categorias': categorias,
            'title': 'produto',
            'busca': busca
        }
        return render(request, 'digistok/cadastra_produto.html', context)
    def post(self, request):
        codigo = request.POST.get('codigo', '').strip()
        foto = request.FILES.get('foto')
        descricao = request.POST.get('descricao', '').strip()
        unidade = request.POST.get('unidade', '').strip()
        fornecedor_id = request.POST.get('fornecedor', '').strip()
        categoria_id = request.POST.get('categoria', '').strip()
        detalhes = request.POST.get('detalhes', '').strip()

        if not codigo:
            messages.error(request, 'Código do produto é obrigatório.')
            return redirect('cadastra_produto')

        if Produto.objects.filter(codigo=codigo).exists():
            messages.error(request, f'O produto com código {codigo} já está cadastrado.')
            return redirect('cadastra_produto')

        # Recupera instâncias de categoria e fornecedor, se existirem
        categoria = Categoria.objects.filter(id=categoria_id).first() if categoria_id else None
        fornecedor = Fornecedor.objects.filter(id=fornecedor_id).first() if fornecedor_id else None

        produto = Produto(
            codigo=codigo,
            foto=foto,
            descricao=descricao,
            unidade_medida=unidade,
            fornecedor=fornecedor,
            categoria=categoria,
            detalhes=detalhes
        )
        produto.save()
        messages.success(request, 'Produto cadastrado com sucesso!')
        return redirect('cadastra_produto')
        
    
# Edita Produto
class EditaProduto(View):
    template_name = 'digistok/cadastra_produto.html'

    def get(self, request, pk):
        produto = get_object_or_404(Produto, pk=pk)
        produtos = Produto.objects.all()
        fornecedores = Fornecedor.objects.all().order_by('id')
        categorias = Categoria.objects.all().order_by('id')
        return render(request, self.template_name, {
            'fornecedores': fornecedores,
            'categorias': categorias,
            'produtos' : produtos,
            'produto' : produto
        })
    def post(self, request, pk):
        produto = get_object_or_404(Produto, pk=pk)

        # Atualização de textos e numeros
        produto.codigo = request.POST.get('codigo')
        produto.descricao = request.POST.get('descricao', '').strip()
        produto.unidade_medida = request.POST.get('unidade', '').strip()
        produto.detalhes = request.POST.get('detalhes', '').strip()
        try:
            produto.codigo = int(request.POST.get('codigo'))
        except (ValueError, TypeError):
            messages.error(request, 'Código deve ser um número válido.')
            fornecedores = Fornecedor.objects.all().order_by('id')
            categorias = Categoria.objects.all().order_by('id')
            produtos = Produto.objects.all()
            return render(request, self.template_name, {
                'fornecedores': fornecedores,
                'categorias': categorias,
                'produtos': produtos,
                'produto': produto
            })

        categoria_id = request.POST.get('categoria')
        fornecedor_id = request.POST.get('fornecedor')

        if categoria_id:
            try:
                produto.categoria = Categoria.objects.get(id=categoria_id)
            except Categoria.DoesNotExist:
                messages.error(request, 'Categoria inválida. Selecione uma categoria existente.')
                fornecedores = Fornecedor.objects.all().order_by('id')
                categorias = Categoria.objects.all().order_by('id')
                produtos = Produto.objects.all()
                return render(request, self.template_name, {
                    'fornecedores': fornecedores,
                    'categorias': categorias,
                    'produtos': produtos,
                    'produto': produto
                })
        else:
            produto.categoria = None

        if fornecedor_id:
            try:
                produto.fornecedor = Fornecedor.objects.get(id=fornecedor_id)
            except Fornecedor.DoesNotExist:
                messages.error(request, 'Fornecedor inválido. Selecione um fornecedor existente.')
                fornecedores = Fornecedor.objects.all().order_by('id')
                categorias = Categoria.objects.all().order_by('id')
                produtos = Produto.objects.all()
                return render(request, self.template_name, {
                    'fornecedores': fornecedores,
                    'categorias': categorias,
                    'produtos': produtos,
                    'produto': produto
                })
        else:
            produto.fornecedor = None

        # Checa campo foto
        if 'foto' in request.FILES:
            produto.foto = request.FILES['foto']
        elif request.POST.get('foto_clear') == 'on':
            produto.foto = None

        # Sava a edição
        produto.save()

        messages.success(request, "Produto atualizado com sucesso!")
        return redirect('cadastra_produto')


# Apaga Produto individual
class ApagaProduto(DeleteView):
    model = Produto
    template_name = 'digistok/cadastra_produto.html'
    success_url = reverse_lazy('cadastra_produto')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        descricao = self.object.descricao
        self.object.delete()
        messages.success(request, f'Produto "{descricao}" apagado com sucesso.')
        return HttpResponseRedirect(self.success_url)
    
    # Apaga a imagem antiga do disco quando o produto for apagado 
    @receiver(post_delete, sender=Produto)
    def apagar_foto(sender, instance, **kwargs):
        if instance.foto and os.path.isfile(instance.foto.path):
            os.remove(instance.foto.path)

    # Apaga a imagem antiga do disco quando a  noticia for atualizada
    @receiver(pre_save, sender=Produto)
    def apagar_antiga(sender, instance, **kwargs):
        if not instance.pk:
            return 

        try:
            foto_antiga = Produto.objects.get(pk=instance.pk).foto
        except Produto.DoesNotExist:
            return

        nova_foto= instance.foto
        if foto_antiga and foto_antiga != nova_foto:
            if os.path.isfile(foto_antiga.path):
                os.remove(foto_antiga.path)

# Apaga múltiplos produtos
@method_decorator(csrf_exempt, name='dispatch')
class ApagaProdutosSelecionados(View):
    def post(self, request):
        ids = request.POST.getlist('produtos_selecionados')
        if ids:
            produtos = Produto.objects.filter(id__in=ids)
            quantidade = produtos.count()
            nome_primeiro = produtos[0].descricao if quantidade == 1 else None
            produtos.delete()
            if quantidade == 1:
                messages.success(request, f'Produto "{nome_primeiro}" apagado com sucesso.')
            else:
                messages.success(request, f'"{quantidade}" produtos apagados com sucesso.')
        else:
            messages.warning(request, "Nenhum produto selecionado para exclusão.")
        return redirect('cadastra_produto')
# Final CRUD PRODUTO------------------------------
    
    
    
    
# INICIO CRUD FORNECEDOR------------------------------
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
# Final CRUD FORNECEDOR------------------------------








# INICIO CRUD CATEGORIA--------------------------------------
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
        nome1 = request.POST.get('categoriaNome', '').strip()
        nome2 = request.POST.get('categoriaCadastra', '').strip()

        nome = nome2 or nome1
        origem = 'cadastra_produto' if nome2 else 'cadastra_categoria'

        if not nome:
            messages.error(request, "O nome da categoria não pode estar em branco.")
            return redirect(origem)

        if Categoria.objects.filter(nome=nome).exists():
            messages.error(request, f'A categoria "{nome}" já está cadastrada.')
            return redirect(origem)

        Categoria.objects.create(nome=nome)
        messages.success(request, f'Categoria "{nome}" salva com sucesso!')
        return redirect(origem)
    
    # def post(self, request):
    #     nome = request.POST.get('categoriaNome', '').strip()
    #     nome_categoria_pagina_cadastra = request.POST.get('categoriaCadastra', '').strip()
    #     if nome or nome_categoria_pagina_cadastra:
    #         existe = Categoria.objects.filter(Q(nome=nome) | Q(nome=nome_categoria_pagina_cadastra)).exists()
    #     if existe:
    #         if nome_categoria_pagina_cadastra:
    #             messages.error(request, f'A categoria "{nome}" já está cadastrada.')
    #             return redirect('cadastra_produto')
    #         else:
    #             messages.error(request, f'A categoria "{nome}" já está cadastrada.')
    #             return redirect('cadastra_categoria')
    #     if nome or nome_categoria_pagina_cadastra:
    #         if nome_categoria_pagina_cadastra:
    #             Categoria.objects.create(nome=nome_categoria_pagina_cadastra)
    #             messages.success(self.request, f'Categoria "{ nome }" salva com sucesso!')
    #             return redirect('cadastra_produto')
    #         else:
    #             Categoria.objects.create(nome=nome)
    #             messages.success(self.request, f'Categoria "{ nome }" salva com sucesso!')
    #             return redirect('cadastra_categoria')
    #     else:
    #         messages.error(self.request, "O nome da categoria não pode estar em branco.")
    #         return redirect('cadastra_categoria')
                     

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
    
# FIM CRUD CATEGORIA --------------------------




# INICIO CRUD MOVIMENTAÇÂO -------------------------
class MovimentacaoEstoqueView(LoginRequiredMixin, View):
    template_name = 'digistok/movimentacao_estoque.html'

    def get(self, request, pk=None):
        movimentacao = None
        if pk:
            movimentacao = get_object_or_404(MovimentacaoEstoque, pk=pk)

        produtos = Produto.objects.all().order_by('descricao')
        
        # Lista de Movimentações
        movimentacoes_list = MovimentacaoEstoque.objects.all().order_by('-data') 
        
        # Busca de Movimentações
        busca = request.GET.get('busca')
        if busca:
            movimentacoes_list = movimentacoes_list.filter(
                Q(tipo__icontains=busca) |
                Q(produto__descricao__icontains=busca) |
                Q(estoque_origem__icontains=busca) |
                Q(estoque_destino__icontains=busca) |
                Q(usuario_responsavel__username__icontains=busca)
            )

        paginator = Paginator(movimentacoes_list, 10)
        page_number = request.GET.get('page')
        movimentacoes = paginator.get_page(page_number)

        context = {
            'movimentacao': movimentacao,
            'produtos': produtos,
            'movimentacoes': movimentacoes,
            'busca': busca,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        if pk:
            movimentacao = get_object_or_404(MovimentacaoEstoque, pk=pk)
        else:
            movimentacao = MovimentacaoEstoque()

        
        movimentacao.tipo = request.POST.get('tipo')
        produto_id = request.POST.get('produto')
        movimentacao.estoque_origem = request.POST.get('estoque_origem', '').strip()
        movimentacao.estoque_destino = request.POST.get('estoque_destino', '').strip()
        movimentacao.detalhes = request.POST.get('detalhes', '').strip()
        movimentacao.usuario_responsavel = request.user

        try:
            movimentacao.produto = Produto.objects.get(id=produto_id)
        except Produto.DoesNotExist:
            messages.error(request, 'Produto inválido. Selecione um produto existente.')
            
            produtos = Produto.objects.all().order_by('descricao')
            movimentacoes_list = MovimentacaoEstoque.objects.all().order_by('-data')
            paginator = Paginator(movimentacoes_list, 10)
            page_number = request.GET.get('page')
            movimentacoes = paginator.get_page(page_number)
            return render(request, self.template_name, {
                'movimentacao': movimentacao,
                'produtos': produtos,
                'movimentacoes': movimentacoes,
            })

        try:
            movimentacao.full_clean() 
            movimentacao.save()
            messages.success(request, "Movimentação salva com sucesso!")
            return redirect('movimentacao_estoque')
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').capitalize()}: {error}")
            
            produtos = Produto.objects.all().order_by('descricao')
            movimentacoes_list = MovimentacaoEstoque.objects.all().order_by('-data')
            paginator = Paginator(movimentacoes_list, 10)
            page_number = request.GET.get('page')
            movimentacoes = paginator.get_page(page_number)
            return render(request, self.template_name, {
                'movimentacao': movimentacao,
                'produtos': produtos,
                'movimentacoes': movimentacoes,
            })

# Don't forget your delete view:
class ApagaMovimentacoesSelecionadasView(LoginRequiredMixin, View):
    def post(self, request):
        movimentacao_ids = request.POST.getlist('movimentacoes_selecionadas')
        if movimentacao_ids:
            # Add a check to prevent deleting if associated with an important record (e.g., protect)
            MovimentacaoEstoque.objects.filter(id__in=movimentacao_ids).delete()
            messages.success(request, "Movimentações selecionadas excluídas com sucesso!")
        else:
            messages.warning(request, "Nenhuma movimentação foi selecionada para exclusão.")
        return redirect('movimentacao_estoque')
