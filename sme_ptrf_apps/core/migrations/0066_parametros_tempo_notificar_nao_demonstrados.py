# Generated by Django 2.2.10 on 2020-07-31 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0065_unidade_diretor_nome'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametros',
            name='tempo_notificar_nao_demonstrados',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Tempo para notificação de transações não demonstradas (dias)'),
        ),
    ]