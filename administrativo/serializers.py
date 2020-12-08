from .models import Loja, Produto, Promocao, CategoriaProduto
from rest_framework import serializers

class LojaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loja
        fields = ['id', 'nome', 'cidade', 'uf', 'email']


class CategoriaProdutoSerializer(serializers.ModelSerializer): #Ainda não vejo necessidade disso, mas estudaremos
    class Meta:
        model = CategoriaProduto
        fields = ['id', 'nome']


class ProdutoSerializer(serializers.ModelSerializer):
    categoria = serializers.SlugRelatedField(many=False, read_only=False, queryset=CategoriaProduto.objects.all(), slug_field="nome")
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'imagem', 'descricao', 'categoria']


class PromocaoSerializer(serializers.ModelSerializer):
    produto = serializers.SlugRelatedField(many=False, read_only=False, queryset=Produto.objects.all(), slug_field="nome")
    loja = serializers.SlugRelatedField(many=False, read_only=False, queryset=Loja.objects.all(), slug_field="nome")
    class Meta:
        model = Promocao
        fields = ['id', 'produto', 'preco', 'loja', 'cupom', 'destaque']
