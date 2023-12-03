from django.contrib import admin
from cotacao.models import Investidor, AtivoB3, TunelPreco, Monitoracao

admin.site.register(Investidor)
admin.site.register(AtivoB3)
admin.site.register(TunelPreco)
admin.site.register(Monitoracao)
# Register your models here.
