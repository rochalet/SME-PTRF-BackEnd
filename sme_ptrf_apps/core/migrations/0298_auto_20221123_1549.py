# Generated by Django 2.2.10 on 2022-11-23 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0297_auto_20221123_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analisedocumentoprestacaoconta',
            name='status_realizacao',
            field=models.CharField(choices=[('PENDENTE', 'Pendente'), ('REALIZADO', 'Realizado'), ('JUSTIFICADO', 'Justificado'), ('REALIZADO_JUSTIFICADO', 'Realizado e justificado'), ('REALIZADO_PARCIALMENTE', 'Realizado parcialmente')], default='PENDENTE', max_length=40, verbose_name='Status de realização'),
        ),
    ]
