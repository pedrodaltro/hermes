from django.db import models
import uuid


class Investidor(models.Model):
    id = models.CharField(primary_key=True,default=uuid.uuid4, editable=False, max_length=36)
    email = models.EmailField(max_length=250)
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class AtivoB3(models.Model):
    sigla = models.CharField(max_length=10, primary_key=True)
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return self.sigla

class Monitoracao(models.Model):
    id = models.CharField(primary_key=True,default=uuid.uuid4, editable=False, max_length=36)
    periodicidade = models.IntegerField()
    investidor = models.ForeignKey(Investidor, on_delete=models.CASCADE)
    ativoB3 = models.ForeignKey(AtivoB3, on_delete=models.CASCADE)
    limiteSuperior = models.IntegerField(default=0)
    limiteInferior = models.IntegerField(default=0)

class Cotacao(models.Model):
    id = models.CharField(primary_key=True,default=uuid.uuid4, editable=False, max_length=36)
    dataHora = models.DateTimeField(blank=True, null=True)
    valor = models.IntegerField(blank=True, null=True)
    monitoracao = models.ForeignKey(Monitoracao, on_delete=models.CASCADE)
