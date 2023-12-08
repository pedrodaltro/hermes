# Generated by Django 4.2.4 on 2023-12-07 02:02

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cotacao', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monitoracao',
            name='ultimo_valor',
        ),
        migrations.CreateModel(
            name='Cotacao',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('dataHora', models.DateTimeField(blank=True, null=True)),
                ('valor', models.IntegerField(blank=True, null=True)),
                ('ativoB3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cotacao.monitoracao')),
            ],
        ),
    ]
