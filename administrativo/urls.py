from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    #Esses dados são ignorados, pois o urls.py do AdmLanchonete dá um 'from administrativo.views import ...', sendo assim, nem cosulta este arquivo.
    #path('', views.areaAdministrativa),
    #path('lojas/', views.LojaList.as_view()),
    path('lojas/', views.LojaList.as_view()),
    path('produtos/', views.ProdutoList.as_view()),
    path('promocoes/', views.PromocoesList.as_view()),
]