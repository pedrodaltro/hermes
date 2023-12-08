from django import forms
from cotacao.models import Investidor, Monitoracao


class InvestidorForm(forms.ModelForm):
    class Meta:
        model = Investidor
        exclude = ["id"]


class MonitoracaoForm(forms.ModelForm):
    class Meta:
        model = Monitoracao
        exclude = ["id", "task", "investidor"]
        labels = {
            "periodicidade": "Períodicidade da consulta em minutos",
            "ativoB3": " Ativo B3",
            "limiteSuperior": " Valor Venda",
            "limiteInferior": " Valor Compra"
        }
