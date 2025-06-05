from django.contrib.auth.models import User
from django.db import models


STATUS_CHOICES = [
    ('Ativo', 'Ativo'),
    ('Inativo', 'Inativo'),
]
TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
        ('TRANSFERENCIA', 'Transferência'),
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
    
    
class MovimentacaoEstoque(models.Model):
    tipo = models.CharField(max_length=20,choices=TIPO_CHOICES)
    produto = models.ForeignKey('Produto',on_delete=models.PROTECT)
    quantidade = models.IntegerField(default=0)
    estoque_origem = models.ForeignKey('Local', on_delete=models.PROTECT, related_name='movimentacoes_origem', blank=True, null=True)
    estoque_destino = models.ForeignKey('Local', on_delete=models.PROTECT, related_name='movimentacoes_destino', blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)
    usuario_responsavel = models.ForeignKey(User,on_delete=models.PROTECT)
    detalhes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.tipo} - {self.produto} - {self.data.strftime("%d/%m/%Y %H:%M")}'

class Local(models.Model):
    descricao = models.CharField(max_length=200)
    endereco = models.CharField(max_length=300)    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Ativo')

    def __str__(self):
        return self.descricao