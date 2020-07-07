# Generated by Django 2.2.10 on 2020-06-08 13:20

import django.contrib.postgres.fields
from django.db import migrations, models

import sme_ptrf_apps.core.models.fechamento_periodo


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_merge_20200608_0027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fechamentoperiodo',
            name='especificacoes_despesas',
        ),
        migrations.AddField(
            model_name='fechamentoperiodo',
            name='especificacoes_despesas_capital',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=sme_ptrf_apps.core.models.fechamento_periodo.get_especificacoes_despesas_default, size=None, verbose_name='especificações das despesas (capital)'),
        ),
        migrations.AddField(
            model_name='fechamentoperiodo',
            name='especificacoes_despesas_custeio',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=sme_ptrf_apps.core.models.fechamento_periodo.get_especificacoes_despesas_default, size=None, verbose_name='especificações das despesas (custeio)'),
        ),
    ]