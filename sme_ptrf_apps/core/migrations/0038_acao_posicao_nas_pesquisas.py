# Generated by Django 2.2.10 on 2020-06-09 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_auto_20200608_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='acao',
            name='posicao_nas_pesquisas',
            field=models.CharField(blank=True, default='ZZZZZZZZZZ', help_text='A ordem alfabética desse texto definirá a ordem que a ação será exibida nas pesquisas.', max_length=10, verbose_name='posição nas pesquisas'),
        ),
    ]