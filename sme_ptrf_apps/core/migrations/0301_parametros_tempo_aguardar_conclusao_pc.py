# Generated by Django 2.2.10 on 2023-01-21 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0300_auto_20230121_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametros',
            name='tempo_aguardar_conclusao_pc',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Quanto tempo deve-se aguardar a conclusão da PC (segundos)?'),
        ),
    ]
