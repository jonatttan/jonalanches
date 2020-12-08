from django.db import models
from django.contrib.auth.models import User

class Loja(models.Model):

    nome = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    email = models.CharField(max_length=100)

    class Meta:
        verbose_name = ("Loja")
        verbose_name_plural = ("Lojas")

    def __str__(self):
        return self.nome


class CategoriaProduto(models.Model):
    
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = ("Categoria")
        verbose_name_plural = ("Categorias")

    def __str__(self):
        return self.nome


class Produto(models.Model):

    nome = models.CharField(max_length=100)
    imagem = models.CharField(max_length=400)
    descricao = models.CharField(max_length=300)
    categoria = models.ForeignKey(CategoriaProduto, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Produto")
        verbose_name_plural = ("Produtos")

    def __str__(self):
        return self.nome


class Promocao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE)
    preco = models.FloatField()#default=8.90)
    cupom = models.CharField(max_length=10, unique=True)#O ideal aqui seria criação automática, atualmente checa se é único
    destaque = models.BooleanField(default=False) #tem de ser BooleanField**

    class Meta:
        verbose_name = ("Promocao")
        verbose_name_plural = ("Promocoes")

    def __str__(self):
        return self.cupom

class Favoritos(models.Model):
    clienteid = models.IntegerField() #Limita ao usuário 99
    promocaoid = models.ForeignKey(Promocao, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = ("Favorito")
        verbose_name_plural = ("Favoritos")

    def __str__(self):
        return self.clienteid
