# Generated by Django 2.2.10 on 2020-08-08 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0072_unidade_dre_diretor_regional_nome'),
    ]

    operations = [
        migrations.AddField(
            model_name='unidade',
            name='dre_designacao_portaria',
            field=models.CharField(blank=True, default='', max_length=160, verbose_name='Designação portaria'),
        ),
    ]