from django.db import models
import uuid


class Investidor(models.Model):
    cpf = models.CharField(max_length=11, primary_key=True)
    email = models.EmailField(max_length=250, default='ok@ok.com')
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.cpf


class AtivoB3(models.Model):
    sigla = models.CharField(max_length=10, primary_key=True)
    descricao = models.CharField(max_length=200)


class TunelPreco(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    limiteSuperior = models.IntegerField()
    limiteInferior = models.IntegerField()


class Monitoracao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    periodicidade = models.IntegerField()
    investidor = models.ForeignKey(Investidor, on_delete=models.SET_NULL,
                                blank=True, null=True)
    ativoB3 = models.ForeignKey(AtivoB3, on_delete=models.SET_NULL, 
                                blank=True, null=True)
    tunelPreco = models.OneToOneField(TunelPreco, on_delete=models.SET_NULL, 
                                      blank=True, null=True)
    ultimo_valor = models.IntegerField(null=True)
