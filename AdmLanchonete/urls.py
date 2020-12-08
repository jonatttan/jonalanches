"""AdmLanchonete URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from administrativo.views import areaAdministrativa, do_login, do_logout, new_user, list_loja, list_produtos, list_promocoes, home, list_favoritos


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('login/', do_login),
    path('logout/', do_logout),
    path('newuser/', new_user),
    path('lojas/', list_loja),
    path('produtos/', list_produtos),
    path('promocoes/', list_promocoes),
    path('administrativo/', areaAdministrativa),
    path('favoritos/', list_favoritos),
    path('api/', include('administrativo.urls')),
    #path('api/', include('administrativo.urls')),
]
