# Generated by Django 2.2.10 on 2022-08-24 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0279_merge_20220823_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='analiselancamentoprestacaoconta',
            name='esclarecimentos',
            field=models.TextField(blank=True, default=None, max_length=300, null=True, verbose_name='Esclarecimentos'),
        ),
        migrations.AddField(
            model_name='analiselancamentoprestacaoconta',
            name='lancamento_atualizado',
            field=models.BooleanField(default=False, verbose_name='Lançamento Atualizado?'),
        ),
        migrations.AddField(
            model_name='analiselancamentoprestacaoconta',
            name='lancamento_excluido',
            field=models.BooleanField(default=False, verbose_name='Lançamento Excluído?'),
        ),
    ]
