from django.db import models

STATUS_CHOICES = [
    ('Ativo', 'Ativo'),
    ('Inativo', 'Inativo'),
]

# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nome


class Fornecedor(models.Model):
    cpf_cnpj = models.CharField(max_length=18, unique=True)
    nome = models.CharField(max_length=100)
    contato = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200)
    cidade = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Ativo')

    def __str__(self):
        return self.nome
