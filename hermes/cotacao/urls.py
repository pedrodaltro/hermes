from django.urls import path, include
from .views import home, salvar, form_modelform, salao_investidor

urlpatterns = [
    path('', home, name='home'),
    path('salvar/', salvar, name='salvar'),
    path('salao_investidor/', salao_investidor, name='salao_investidor'),
    path('modelform/', form_modelform, name='form_modelform'),
]
