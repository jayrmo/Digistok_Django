from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import *
import datetime

# Create your views here.

# def login(request):
#     context = {
#         'title':'Login'
#     }
#     return render(request, 'login.html',context)


class HomePage(View):
    def get(self, request):
        return render(request, 'noticias/homepage.html') 



class Login(View):
    def get(self, request):
        print(f'dentro do get')
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('dentro do post')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
            if messages.get_messages(request):
                primeira_mensagem = list(messages.get_messages(request))[0]
            context = {'primeira_mensagem': primeira_mensagem}
            print(f'dentro do else{username}:{password}')
            return render(request, 'login.html', context)
        