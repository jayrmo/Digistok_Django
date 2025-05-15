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
        noticias = Noticia.objects.all().order_by('-data_publicacao')
        context = {
            'title': 'Home',
            'noticias': noticias,
        }
        return render(request, 'noticias/homepage.html', context) 



# Mostra Formulário
@method_decorator(never_cache, name='dispatch')
class Noticia_form(LoginRequiredMixin, View):
    def get(self, request):
        categorias = Categoria.objects.all()
        context = {
            'title' : 'Adicionar',
            'categorias': categorias,
        }
        return render(request, 'noticias/noticia_form.html', context) 


# Mostra Home do usuário Logado
class HomeAdmView(LoginRequiredMixin, ListView):
    model = Noticia
    template_name = 'noticias/home_adm.html'
    context_object_name = 'noticias'
    
    def get_queryset(self):
        return Noticia.objects.filter(autor=self.request.user)
    
    
# Persiste no DB as Noticias
class NoticiaCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'noticia_form.html')
    

    def post(self, request):
        titulo = request.POST.get('titulo')
        subtitulo = request.POST.get('subtitulo')
        conteudo = request.POST.get('conteudo')
        autor = request.user
        fonte = request.POST.get('fonte')
        local = request.POST.get('local')
        categoria_id = request.POST.get('categoria')
        imagem = request.FILES.get('imagem_url')

        Noticia.objects.create(
            titulo=titulo,
            subtitulo=subtitulo,
            conteudo=conteudo,
            autor=autor,
            fonte=fonte,
            local=local,
            imagem_url=imagem,
            categoria_id=categoria_id  # aceita ID diretamente
        )
        
        messages.success(self.request, "Notícia salva com sucesso!")
        

        return redirect('home_adm')

# Editar Noticia
class NoticiaUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    model = Noticia
    template_name = 'noticias/noticia_form.html'  # caminho correto do template

    def get(self, request, pk):
        noticia = get_object_or_404(Noticia, pk=pk)
        categorias = Categoria.objects.all()
        return render(request, self.template_name, {'noticia': noticia, 'categorias': categorias})

    def post(self, request, pk):
        noticia = get_object_or_404(Noticia, pk=pk)

        # Atualiza os campos com os dados enviados no form
        noticia.titulo = request.POST.get('titulo')
        noticia.subtitulo = request.POST.get('subtitulo')
        noticia.conteudo = request.POST.get('conteudo')
        noticia.fonte = request.POST.get('fonte')
        noticia.local = request.POST.get('local')
        categoria_id = request.POST.get('categoria')
        noticia.categoria_id = categoria_id

        # Se uma nova imagem foi enviada, substitui
        if request.FILES.get('imagem_url'):
            noticia.imagem_url = request.FILES.get('imagem_url')

        noticia.save()

        messages.success(request, "Notícia atualizada com sucesso!")
        return redirect('home_adm')

    def test_func(self):
        noticia = get_object_or_404(Noticia, pk=self.kwargs['pk'])
        return noticia.autor == self.request.user
    
    
    
    
    
# Apagar Noticia
class NoticiaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Noticia
    template_name = 'noticias/noticia_confirm_delete.html'
    success_url = reverse_lazy('home_adm')
    

    def test_func(self):
        noticia = self.get_object()
        return noticia.autor == self.request.user
 

# Apaga a imagem antiga do disco quando a noticia for apagada 
@receiver(post_delete, sender=Noticia)
def apagar_imagem(sender, instance, **kwargs):
    if instance.imagem_url and os.path.isfile(instance.imagem_url.path):
        os.remove(instance.imagem_url.path)

# Apaga a imagem antiga do disco quando a  noticia for atualizada
@receiver(pre_save, sender=Noticia)
def apagar_imagem_antiga(sender, instance, **kwargs):
    if not instance.pk:
        return 

    try:
        imagem_antiga = Noticia.objects.get(pk=instance.pk).imagem_url
    except Noticia.DoesNotExist:
        return

    nova_imagem = instance.imagem_url
    if imagem_antiga and imagem_antiga != nova_imagem:
        if os.path.isfile(imagem_antiga.path):
            os.remove(imagem_antiga.path)    