# Generated by Django 2.2.10 on 2021-06-16 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0182_auto_20210616_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodo',
            name='notificacao_proximidade_inicio_pc_realizada',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Notificação proximidade início PC realizada'),
        ),
    ]
