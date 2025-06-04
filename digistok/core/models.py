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


class Produto(models.Model):
    codigo = models.IntegerField(unique=True)
    descricao = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='produtos/', blank=True, null=True)
    unidade_medida = models.CharField(max_length=200)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    detalhes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.descricao