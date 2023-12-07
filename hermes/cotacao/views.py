from django.shortcuts import render, redirect
from .forms import InvestidorForm, MonitoracaoForm
from .models import Investidor, Monitoracao, Cotacao


def home(request):
    investidores = Investidor.objects.all()
    context = {
        'investidores': investidores
    }
    return render(request, 'index.html', context=context)


def ativo(request):
    if request.method == "POST":
        form = MonitoracaoForm(request.POST)
        if form.is_valid():
            form.save()
    monitoracao_id = request.GET.get('monitoracao')
    cotacoes = Cotacao.objects.filter(monitoracao=monitoracao_id)
    if not cotacoes:
        ativoB3 = Monitoracao.objects.get(id=monitoracao_id).ativoB3_id
    else:
        ativoB3 = cotacoes.first().monitoracao.ativoB3_id
    form = MonitoracaoForm()
    context = {
        'form': form,
        'ativoB3': ativoB3,
        'cotacoes': cotacoes
    }
    return render(request, 'ativo.html', context=context)


def salao_investidor(request, id):
    if request.method == 'GET':
        investidor = Investidor.objects.get(id=id)
        monitoracoes = Monitoracao.objects.filter(investidor=id)
        form = MonitoracaoForm()
        context = {
            'form': form,
            'investidor': investidor,
            'monitoracoes': monitoracoes
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
        context = {
            'form': form,
            'investidor': investidor,
            'ativos_monitorados': ativos_monitorados
        }
        return render(request, 'salao_investidor.html', context=context)


def cadastrar_investidor(request):
    if request.method == "POST":
        form = InvestidorForm(request.POST)
        if form.is_valid():
            form.save()
            investidores = Investidor.objects.all()
            context = {
                'investidores': investidores
            }
            return render(request, 'index.html', context=context)

    form = InvestidorForm()
    context = {
        'form': form
    }
    return render(request, 'cadastrar_investidor.html', context=context)


def editar_investidor(request, id):
    investidor = Investidor.objects.get(id=id)
    if request.method == 'POST':
        form = InvestidorForm(request.POST, instance=investidor)
        if form.is_valid():
            form.save()
            investidores = Investidor.objects.all()
            context = {
                'investidores': investidores
            }
            return render(request, 'index.html', context=context)
    context = {'form': InvestidorForm(instance=investidor), 'id': id}
    return render(request, 'editar_investidor.html', context)


def excluir_investidor(request, id):
    print(id)
    investidor = Investidor.objects.get(id=id)
    print('investidor', investidor)
    investidor.delete()
    investidores = Investidor.objects.all()
    context = {
        'investidores': investidores
    }
    return render(request, 'index.html', context=context)


def cadastrar_monitoracao(request):
    pass


def editar_monitoracao(request, pk):
    pass


def excluir_monitoracao(request, pk):
    pass
