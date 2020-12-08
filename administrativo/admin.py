from django.contrib import admin
from .models import Loja, Produto, Promocao, CategoriaProduto, Favoritos


class LojaAdmin(admin.ModelAdmin):
    list_display = ("nome", "cidade", "uf", "email")

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "imagem", "descricao", "categoria")

class CategoriaProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome",)

class PromocaoAdmin(admin.ModelAdmin):
    list_display = ("produto", "loja", "preco", "cupom", "destaque")

class FavoritosAdmin(admin.ModelAdmin):
    list_display = ("clienteid", "promocaoid")

admin.site.register(Loja, LojaAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(CategoriaProduto, CategoriaProdutoAdmin)
admin.site.register(Promocao, PromocaoAdmin)
admin.site.register(Favoritos, FavoritosAdmin)