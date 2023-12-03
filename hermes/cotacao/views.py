from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from .models import Investidor
# import pandas as pd
import pandas_datareader.data as pdr
import yfinance


yfinance.pdr_override()


def home(request):
    investidores = Investidor.objects.all()
    return render(request, 'index.html', {'investidores': investidores})


def salvar(request):
    novo_investidor = Investidor()
    novo_investidor.email = request.POST.get('email')
    novo_investidor.nome = request.POST.get('nome')
    novo_investidor.cpf = request.POST.get('cpf')
    novo_investidor.save()

    investidores = Investidor.objects.all()
    return render(request, 'index.html', {'investidores': investidores})


def cotar(request):
    resultado = pegar_cotacao(["VALE3.SA", "PETR3.SA", "BVSP"])
    print(resultado)
    return HttpResponse(resultado)


def pegar_cotacao(ativos):
    data = datetime.now()
    tabela_cotacoes = pdr.get_data_yahoo(ativos, data, data)

    return tabela_cotacoes
