from celery import shared_task
from django.http import HttpResponse
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail as sm
#import pandas_datareader.data as pdr
import yfinance as yf
from cotacao.models import Monitoracao, Cotacao

#yfinance.pdr_override()

@shared_task(name="enviar_email", bind=True, default_retry_delay=300, max_retries=5)
def enviar_email(self, subject, message):

    # Fetch all users except superuser
    #users = User.objects.exclude(is_superuser=True).all()
    user_emails = ['pedro.daltro@gmail.com', 'pedro.daltro@live.com']

    # try sending email
    try:
        res = sm(
            subject=subject,
            html_message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=user_emails,
            fail_silently=False,
            message=None)
        print(f'Email send to {len(user_emails)} users')
    except Exception:

        # retry when fail
        enviar_email.retry()

@shared_task(name="send_notification", bind=True, default_retry_delay=300, max_retries=5)
def checar_tunel_preco(id_monitoracao):
    try:
        monitoracao = Monitoracao.objects.get(id_monitoracao=id_monitoracao)
        sigla = monitoracao.ativoB3.sigla
        data = datetime.now()
        cotacao = yf.download(sigla, start=data, end=data)
        valor = cotacao['Close']
        Cotacao.objects.create(dataHora=data, valor=100, monitoracao=id_monitoracao)
        if valor < monitoracao.limiteInferior:
            mensagem = f'Chegou a hora boa para comprar a ação {sigla}'
            enviar_email(mensagem, mensagem)
        elif valor < monitoracao.limiteSuperior:
            mensagem = f'Chegou a hora boa para vender a ação {sigla}'
            enviar_email(mensagem, mensagem)

    except Exception:
        checar_tunel_preco.retry()


    #resultado = pegar_cotacao(["VALE3.SA", "PETR3.SA", "BVSP"])
