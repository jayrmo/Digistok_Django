from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import View
from .models import *

# Create your views here.

@method_decorator(never_cache, name='dispatch')
class HomePage(View):
    def get(self, request): 
        context = {
            'title' : 'Home'
        }
        return render(request, 'noticias/homepage.html', context) 
        # if request.user.is_authenticated:
        #     return HttpResponse("LOGADO como: " + str(request.user.username)), render(request, 'noticias/homepage.html')
        # else:
        #     return HttpResponse("NÃO está logado."),render(request, 'noticias/homepage.html')

@method_decorator(never_cache, name='dispatch')
class Adicionar(View):
    def get(self, request):
        context = {
            'title' : 'Adicionar'
        }
        return render(request, 'noticias/adicionar.html', context) 

        