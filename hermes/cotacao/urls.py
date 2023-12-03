from django.urls import path, include
from .views import home, salvar

urlpatterns = [
    path('', home, name='home'),
    path('salvar/', salvar, name='salvar'),
]
