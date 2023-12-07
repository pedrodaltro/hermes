from celery import shared_task
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail as sm
import yfinance as yf
from cotacao.models import Monitoracao, Cotacao


@shared_task(name="enviar_email", bind=True, default_retry_delay=120, max_retries=3)
def enviar_email(self, titulo, mensagem, email):
    # try sending email
    try:
        res = sm(
            subject=titulo,
            html_message=mensagem,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
            message=None)
    except Exception:

        # retry when fail
        enviar_email.retry()


@shared_task(name="checar_tunel_preco", bind=True, default_retry_delay=120, max_retries=3)
def checar_tunel_preco(self, id_monitoracao):
    try:
        monitoracao = Monitoracao.objects.get(id=id_monitoracao)
        ativo_b3 = monitoracao.ativoB3.sigla
        valor = cotar(ativo_b3)
        Cotacao.objects.create(valor=valor, monitoracao=monitoracao)
        if valor < monitoracao.limiteInferior:
            titulo = f'Oportunidade de compra da ação {ativo_b3}'
            mensagem = f'A ação {ativo_b3}, atingiu o preço para compra'
            enviar_email.delay(mensagem, mensagem)
        elif valor < monitoracao.limiteSuperior:
            titulo = f'Oportunidade de venda da ação {ativo_b3}'
            mensagem = f'A ação {ativo_b3}, atingiu o preço para venda'

            enviar_email.delay(titulo, mensagem, monitoracao.investidor.email)

    except Exception:
        checar_tunel_preco.retry()

def cotar(acao):
    a = yf.Ticker(acao)
    d = a.info
    return d['currentPrice']
