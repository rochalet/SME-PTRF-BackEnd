# Generated by Django 2.2.10 on 2021-06-29 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('despesas', '0035_auto_20210624_1532'),
        ('receitas', '0032_remove_receita_saida_do_recurso'),
    ]

    operations = [
        migrations.AddField(
            model_name='receita',
            name='saida_do_recurso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receitas_saida_do_recurso', to='despesas.Despesa', verbose_name='Saída do Recurso (Despesa)'),
        ),
    ]
