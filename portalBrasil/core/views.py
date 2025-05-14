from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import View
from .models import *

# Create your views here.

@method_decorator(never_cache, name='dispatch')
class HomePage(View):
    def get(self, request):
        return render(request, 'noticias/homepage.html') 
        # if request.user.is_authenticated:
        #     return HttpResponse("LOGADO como: " + str(request.user.username)), render(request, 'noticias/homepage.html')
        # else:
        #     return HttpResponse("NÃO está logado."),render(request, 'noticias/homepage.html')




        