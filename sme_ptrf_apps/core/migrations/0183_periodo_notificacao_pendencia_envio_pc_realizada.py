# Generated by Django 2.2.10 on 2021-06-16 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0182_auto_20210616_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodo',
            name='notificacao_pendencia_envio_pc_realizada',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Notificação pendência envio PC realizada'),
        ),
    ]
