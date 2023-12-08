from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid


class Investidor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    periodicidade = models.PositiveIntegerField(default=1,
        validators=[MaxValueValidator(60), MinValueValidator(1)])
    investidor = models.ForeignKey(Investidor, on_delete=models.CASCADE)
    ativoB3 = models.ForeignKey(AtivoB3, on_delete=models.CASCADE)
    limiteSuperior = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True, default=0.00)
    limiteInferior = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True, default=0.00)
    task = models.BigIntegerField(default=0)

class Cotacao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    dataHora = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=19, decimal_places=2)
    monitoracao = models.ForeignKey(Monitoracao, on_delete=models.CASCADE)
