from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import LojaSerializer, ProdutoSerializer, CategoriaProdutoSerializer, PromocaoSerializer
from .models import Loja, Produto, Promocao, CategoriaProduto, Favoritos

from django.contrib.auth.models import User, Group


class LojaList(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        get_data = request.query_params
        lojas = Loja.objects.all()
        if 'uf' in get_data:
            lojas = lojas.filter(uf=get_data.get('uf'))
        serializer = LojaSerializer(lojas, many=True)
        return Response(serializer.data)

class ProdutoList(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        get_data = request.query_params
        produtos = Produto.objects.all()
        if 'id' in get_data:
            produtos = produtos.filter(id=get_data.get('id'))
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data)

class PromocoesList(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        get_data = request.query_params
        promocoes = Promocao.objects.all()
        if 'id' in get_data:
            promocoes = promocoes.filter(id=get_data.get('id'))
        if 'cup' in get_data:
            promocoes = promocoes.filter(cupom=get_data.get('cup'))
        serializer = PromocaoSerializer(promocoes, many=True)
        return Response(serializer.data)


def do_login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return redirect('/login?erro=true')
    else:
        mensagem_erro = 'Reveja suas credenciais!' if 'erro' in request.GET else ''
    return render(request, 'login.html', {'mensagem_erro': mensagem_erro})

def do_logout (request):
    logout(request)
    #return redirect('/login')
    return redirect('/')

def new_user(request):
    if request.method == 'POST':
        #Recebe dados do usuário
        nome = request.POST["name"]
        mail = request.POST["mail"]
        username = request.POST["user"]
        password = request.POST["passwd"]
        if User.objects.filter(username=username).exists():
            mensagem = 'Escolha outro nome de usuário.'
        else:
            user = User.objects.create_user(username, mail, password)
            #Pega o objeto usuário e seta o atributo abaixo
            user.first_name = nome
            user.save()
            #user.permissions.
            #Insere o usuário no grupo cliente
            grupo = Group.objects.get(name="cliente")
            grupo.user_set.add(user)
            mensagem = 'Usuario criado com sucesso!'
        return render(request, 'newuser.html', {'mensagem': mensagem})
        #return redirect(do_login)
    else:
        return render(request, 'newuser.html')


def areaAdministrativa(request):

    if not request.user.is_authenticated:
        return redirect('/login')
    grupo = Group.objects.get(name="administradores")
    lojas = Loja.objects.all()#Para implementar limite, usar: [:3]
    produtos = Produto.objects.all()
    promocoes = Promocao.objects.all()
    categorias = CategoriaProduto.objects.all()

    if request.method == "POST":
        if "taskAddLoja" in request.POST:
            lojaNome = request.POST["nomeLoja"]
            lojaCidade = request.POST["cidadeLoja"]
            lojaUf = request.POST["estadoLoja"]
            lojaEmail = request.POST["emailLoja"]
            regLoja = Loja(nome=lojaNome, cidade=lojaCidade, uf=lojaUf, email=lojaEmail)
            regLoja.save()
            return redirect("../administrativo/")
        
        if "taskDeleteLoja" in request.POST:
            checkedlist = request.POST["checkedbox"]
            for lojaId in checkedlist:
                delLoja = Loja.objects.get(id=int(lojaId))
                delLoja.delete()

        if "taskAddProduto" in request.POST:
            produtoNome = request.POST["nomeProduto"]
            produtoDescricao = request.POST["descricaoProduto"]
            produtoCategoria = request.POST["categoriaProduto"]
            if request.POST["imagemProduto"] == "":
                produtoImagem = "..\static\images\img_produtos\default-image.png"
            else:
                produtoImagem = request.POST["imagemProduto"]
            regProduto = Produto(nome=produtoNome, imagem=produtoImagem, descricao=produtoDescricao, categoria=CategoriaProduto.objects.get(id=produtoCategoria))
            regProduto.save()
            return redirect("../administrativo/")

        if "taskDeleteProduto" in request.POST:
            checkedlist = request.POST["checkedbox"]
            for produtoId in checkedlist:
                delProduto = Produto.objects.get(id=int(produtoId))
                delProduto.delete()

        if "taskAddPromocao" in request.POST:
            promoProd = request.POST["prodPromo"]
            promoLoja = request.POST["lojaPromo"]
            promoPreco = request.POST["precoPromo"]
            promoCupom = request.POST["cupomPromo"]
            promoDestaque = request.POST["destaquePromo"]
            regPromo = Promocao(produto=Produto.objects.get(id=promoProd), loja=Loja.objects.get(id=promoLoja), preco=promoPreco, cupom=promoCupom, destaque=promoDestaque)
            regPromo.save()
            return redirect("../administrativo/")
           
        if "taskDeletePromocao" in request.POST:
            checkedlist = request.POST["checkedbox"]
            for promoId in checkedlist:
                delPromo = Promocao.objects.get(id=int(promoId))
                delPromo.delete()

    #return render(request, "administrativo.html")
    return render(request, "administrativo.html", {"lojas":lojas, "produtos":produtos, "promocoes":promocoes, "categorias":categorias, "grupo": grupo})
    

def list_loja(request):
    grupo = Group.objects.get(name="administradores")
    lojas = Loja.objects.all()
    lojasFiltradas = lojas

    if request.method == "POST":
        if "filtraLojas" in request.POST:
            findName = request.POST["nomeLoja"]
            findCidade = ""
            findUf = ""

            if request.POST["ufLoja"] != "":
                findUf = request.POST["ufLoja"]

            if request.POST["cidadeLoja"] != "":
                findCidade = request.POST["cidadeLoja"]

            lojasFiltradas = Loja.objects.filter(nome__contains=findName, cidade__contains=findCidade, uf__contains=findUf)
                #lojas = Loja.objects.filter(uf__contains="SC")
            
                
    return render(request, 'lojas.html', {"lojas":lojas, "lojasFiltradas":lojasFiltradas, "grupo": grupo})

def list_produtos(request):
    grupo = Group.objects.get(name="administradores")
    produtos = Produto.objects.all()
    produtosFiltrados = produtos
    produtoCategoria = CategoriaProduto.objects.all()

    if request.method == "POST":
        if "filtraProdutos" in request.POST:
            findName = ""
            findCategory = ""

            if request.POST["nomeProduto"] != "":
                findName = request.POST["nomeProduto"]
            if request.POST["categoriaProduto"] != "":
                findCategory = request.POST["categoriaProduto"]
                produtosFiltrados = Produto.objects.filter(nome__contains=findName, categoria=findCategory)
                return render(request, 'produtos.html', {"produtos": produtos, "produtosFiltrados": produtosFiltrados, "produtoCategoria": produtoCategoria})

            produtosFiltrados = Produto.objects.filter(nome__contains=findName)
            
    return render(request, 'produtos.html', {"produtos": produtos, "produtosFiltrados": produtosFiltrados, "produtoCategoria": produtoCategoria, "grupo": grupo})

def list_promocoes(request):
    grupo = Group.objects.get(name="administradores")
    promocoes = Promocao.objects.all().order_by('-destaque')
    promocoesFiltradas = promocoes
    lojas = Loja.objects.all()
    findPrice = ""

    if request.method == "POST":
        
        #findName = request.POST["nomePromo"]

        if "filtraPromos" in request.POST:
            findLoja = request.POST["lojaPromo"]
            findPrice = request.POST["precoPromo"]

            if findPrice == "1":
                #findPrice = request.POST["precoPromo"]
                promocoesFiltradas = promocoesFiltradas.order_by('-preco')
            else:
                promocoesFiltradas = promocoesFiltradas.order_by('preco')

            if findLoja != "":            
                promocoesFiltradas = Promocao.objects.filter(loja=findLoja)
            
            #if findName != "":
            #    findprod=Produto.objects.filter(nome__contains=findName)
            #    promocoesFiltradas = promocoesFiltradas.filter(findprod.get(id))

        if "taskAddFavorito" in request.POST:
            userId = request.user.id
            promoId = request.POST["idPromo"]

            favorito = Favoritos(clienteid=userId, promocaoid=Promocao.objects.get(id=promoId))
            favorito.save()

    return render(request, 'promocoes.html', {"promocoes": promocoes, "promocoesFiltradas": promocoesFiltradas, "lojas": lojas, "grupo": grupo})

def home(request):

    grupo = Group.objects.get(name="administradores")

    #promoDestaque = Promocao.objects.filter(destaque__contains='1')
    promoOrderDestaque = Promocao.objects.all().order_by('-destaque')[:5] #filter(destaque=0)
    produtos = Produto.objects.all()[:5]

    #promoDestaque = Produto.objects.all()
    #produtosFiltrados = produtos
    #produtoCategoria = CategoriaProduto.objects.all()

    #return render(request, 'produtos.html', {"produtos": produtos, "produtosFiltrados": produtosFiltrados, "produtoCategoria": produtoCategoria, "grupo": grupo})    
    
    return render(request, 'home.html', {"grupo": grupo, "promoDestaque": promoOrderDestaque, "produtos": produtos})
    #grupo = Group.objects.get(name="administradores")
    #, "grupo": grupo

def list_favoritos(request):
    grupo = Group.objects.get(name="administradores")
    user = request.user.id
    favoritos = Favoritos.objects.filter(clienteid=user)
    #favoritos = Favoritos.objects.all()

    if "taskDeleteFavorito" in request.POST:
        item = request.POST["idFavorito"]
        delFavorito = Favoritos.objects.get(id=int(item))
        delFavorito.delete()

    return render(request, 'favoritos.html', {"grupo": grupo, "favoritos": favoritos})
