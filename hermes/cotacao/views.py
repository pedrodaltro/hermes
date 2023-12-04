from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse

from .forms import InvestidorForm, MonitoracaoForm
from .models import Investidor, AtivoB3, Monitoracao
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


def form_modelform(request):
    if request.method == "GET":
        form = InvestidorForm()
        context = {
            'form': form
        }
        return render(request, 'formulario_modelform.html', context=context)
    else:
        form = InvestidorForm(request.POST)
        if form.is_valid():
            investidor = form.save()
            form = InvestidorForm()
        context = {
            'form': form
        }
        return render(request, 'formulario_modelform.html', context=context)


def salao_investidor(request):
    if request.method == 'GET':
        cpf_investidor = request.GET.get('investidor')
        investidor = Investidor.objects.get(cpf__exact=cpf_investidor)
        ativos_monitorados = Monitoracao.objects.filter(investidor=cpf_investidor)
        form = MonitoracaoForm()
        context = {
            'form': form,
            'investidor': investidor,
            'ativos_monitorados': ativos_monitorados
        }
        return render(request, 'salao_investidor.html', context=context)
    else:
        form = MonitoracaoForm(request.POST)
        id_investidor = request.POST.get('id_investidor')
        investidor = Investidor.objects.get(cpf__exact=id_investidor)
        ativos_monitorados = Monitoracao.objects.filter(investidor=id_investidor)
        if form.is_valid():
            monitoracao = form.save(commit=False)
            monitoracao.investidor = investidor
            monitoracao.save()
            form = MonitoracaoForm()
        ativos_b3 = AtivoB3.objects.all()
        context = {
            'form': form,
            'investidor': investidor,
            'ativos_monitorados': ativos_monitorados
        }
        return render(request, 'salao_investidor.html', context=context)
