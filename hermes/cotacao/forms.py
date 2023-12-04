from django import forms
from cotacao.models import Investidor, Monitoracao


class InvestidorForm(forms.ModelForm):
    class Meta:
        model = Investidor
        fields = "__all__"


class MonitoracaoForm(forms.ModelForm):
    class Meta:
        model = Monitoracao
        exclude = ["id", "ultimo_valor", "investidor"]
        labels = {
            "periodicidade": "Período da consulta em minutos",
            "investidor": "Investidor",
            "ativoB3": " Ativo B3",
            "limiteSuperior": " Valor Venda",
            "limiteInferior": " Valor Compra"
        }
