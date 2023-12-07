from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('salao_investidor/<str:id>', salao_investidor, name='salao_investidor'),
    path('ativo', ativo, name='ativo'),
    path('cadastrar_investidor', cadastrar_investidor, name='cadastrar_investidor'),
    path('editar_investidor/<str:id>', editar_investidor, name='editar_investidor'),
    path('excluir_investidor/<str:id>', excluir_investidor, name='excluir_investidor'),
    path('cadastrar_monitoracao', cadastrar_monitoracao, name='cadastrar_monitoracao'),
    path('editar_monitoracao/<str:id>', editar_monitoracao, name='editar_monitoracao'),
    path('excluir_monitoracao/<str:id>', excluir_monitoracao, name='excluir_monitoracao'),
]
