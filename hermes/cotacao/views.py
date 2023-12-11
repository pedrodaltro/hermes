import json
from django.shortcuts import render
from django.contrib import messages
from .forms import InvestidorForm, MonitoracaoForm
from .models import Investidor, Monitoracao, Cotacao
from django_celery_beat.models import PeriodicTask,  CrontabSchedule


def home(request):
    investidores = Investidor.objects.all()
    context = {
        'investidores': investidores
    }
    return render(request, 'index.html', context=context)


def salao_investidor(request, id_investidor):
    if request.method == 'GET':
        investidor = Investidor.objects.get(id=id_investidor)
        print('Aqui', investidor)
        monitoracoes = Monitoracao.objects.filter(investidor=id_investidor)
        context = {
            'investidor': investidor,
            'monitoracoes': monitoracoes
        }
        return render(request, 'salao_investidor.html', context=context)


def historico_cotacoes(request, id_monitoracao):
    cotacoes = Cotacao.objects.filter(monitoracao=id_monitoracao)
    if not cotacoes:
        monitoracao = Monitoracao.objects.get(id=id_monitoracao)
        ativo_b3 = monitoracao.ativoB3_id
        investidor = monitoracao.investidor
    else:
        ativo_b3 = cotacoes.first().monitoracao.ativoB3_id
        investidor = cotacoes.first().monitoracao.investidor
    form = MonitoracaoForm()
    context = {
        'form': form,
        'ativo_b3': ativo_b3,
        'cotacoes': cotacoes,
        'investidor': investidor
    }
    return render(request, 'cotacoes.html', context=context)


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


def editar_investidor(request, id_investidor):
    investidor = Investidor.objects.get(id=id_investidor)
    if request.method == 'POST':
        form = InvestidorForm(request.POST, instance=investidor)
        if form.is_valid():
            form.save()
            investidores = Investidor.objects.all()
            context = {
                'investidores': investidores
            }
            return render(request, 'index.html', context=context)
    context = {'form': InvestidorForm(instance=investidor), 'id': id_investidor}
    return render(request, 'editar_investidor.html', context)


def excluir_investidor(request, id_investidor):
    investidor = Investidor.objects.get(id=id_investidor)
    investidor.delete()
    investidores = Investidor.objects.all()
    context = {
        'investidores': investidores
    }
    return render(request, 'index.html', context=context)


def cadastrar_monitoracao(request, id_investidor):
    if request.method == "POST":
        investidor = Investidor.objects.get(id=id_investidor)
        form = MonitoracaoForm(request.POST)
        if form.is_valid():
            monitoracao = form.save(commit=False)
            monitoracao.investidor = investidor
            monitoracao.save()
            monitoracao.task = cadastrar_task_cotacao(monitoracao.ativoB3.sigla, monitoracao.investidor.id,
                                                      monitoracao.periodicidade, monitoracao.id)
            monitoracao.save()
            form.save()
            monitoracoes = Monitoracao.objects.filter(investidor=id_investidor)
            context = {
                'monitoracoes': monitoracoes,
                'investidor': investidor
            }
            return render(request, 'salao_investidor.html', context=context)
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request, 'cadastrar_monitoracao.html', context={'form': form, 'id_investidor': id_investidor})
    form = MonitoracaoForm()
    context = {
        'form': form,
        'id_investidor': id_investidor
    }
    return render(request, 'cadastrar_monitoracao.html', context=context)


def editar_monitoracao(request, id_monitoracao):
    monitoracao = Monitoracao.objects.get(id=id_monitoracao)
    if request.method == 'POST':
        investidor = Investidor.objects.get(id=monitoracao.investidor.id)
        form = MonitoracaoForm(request.POST, instance=monitoracao)
        if form.is_valid():
            form.save()
            monitoracoes = Monitoracao.objects.all()
            context = {
                'monitoracoes': monitoracoes,
                'investidor': investidor
            }
            return render(request, 'salao_investidor.html', context=context)
    context = {
        'form': MonitoracaoForm(instance=monitoracao),
        'id_monitoracao': id_monitoracao
    }
    return render(request, 'editar_monitoracao.html', context)


def excluir_monitoracao(request, id_monitoracao):
    monitoracao = Monitoracao.objects.get(id=id_monitoracao)
    investidor = Investidor.objects.get(id=monitoracao.investidor.id)
    tarefa_agendada = PeriodicTask.objects.filter(id=monitoracao.task)
    if tarefa_agendada is not None:
        tarefa_agendada.delete()
    monitoracao.delete()
    monitoracoes = Monitoracao.objects.all()
    context = {
        'monitoracoes': monitoracoes,
        'investidor': investidor
    }
    return render(request, 'salao_investidor.html', context=context)


def cadastrar_task_cotacao(ativo_b3, id_investidor, tempo, id_monitoracao):
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=f'*/{tempo}',
        hour='*',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*',
        timezone='America/Sao_Paulo'
    )
    task = PeriodicTask.objects.create(
        crontab=schedule,
        name=f'{ativo_b3}_{id_monitoracao}',
        task='checar_tunel_preco',
        args=json.dumps([f'{id_monitoracao}']),
    )
    print('A task', task.id)
    return task.id

