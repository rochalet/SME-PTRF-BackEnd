# Generated by Django 2.2.10 on 2022-08-29 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0280_auto_20220824_0855'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestacaoconta',
            name='justificativa_pendencia_realizacao',
            field=models.TextField(blank=True, default='', verbose_name='Justificativa de pendências de realização de ajustes.'),
        ),
    ]
