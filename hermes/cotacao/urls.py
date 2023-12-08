from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('salao_investidor/<str:id_investidor>', salao_investidor, name='salao_investidor'),
    path('historico_cotacoes/<str:id_monitoracao>', historico_cotacoes, name='historico_cotacoes'),
    path('cadastrar_investidor', cadastrar_investidor, name='cadastrar_investidor'),
    path('editar_investidor/<str:id_investidor>', editar_investidor, name='editar_investidor'),
    path('excluir_investidor/<str:id_investidor>', excluir_investidor, name='excluir_investidor'),
    path('cadastrar_monitoracao/<str:id_investidor>', cadastrar_monitoracao, name='cadastrar_monitoracao'),
    path('editar_monitoracao/<str:id_monitoracao>', editar_monitoracao, name='editar_monitoracao'),
    path('excluir_monitoracao/<str:id_monitoracao>', excluir_monitoracao, name='excluir_monitoracao'),
]
