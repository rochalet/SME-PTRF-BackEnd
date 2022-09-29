# Generated by Django 2.2.10 on 2022-09-23 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0270_remove_prestacaoconta_devolucao_tesouro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arquivo',
            name='tipo_carga',
            field=models.CharField(choices=[('REPASSE_REALIZADO', 'Repasses realizados'), ('CARGA_PERIODO_INICIAL', 'Carga período inicial'), ('REPASSE_PREVISTO', 'Repasses previstos'), ('CARGA_ASSOCIACOES', 'Carga de Associações'), ('CARGA_USUARIOS', 'Carga de usuários'), ('CARGA_CENSO', 'Carga de censo'), ('CARGA_REPASSE_PREVISTO_SME', 'Repasses previstos sme'), ('CARGA_DEVOLUCAO_TESOURO', 'Devoluções ao Tesouro')], default='REPASSE_REALIZADO', max_length=35, verbose_name='tipo de carga'),
        ),
        migrations.AlterField(
            model_name='modelocarga',
            name='tipo_carga',
            field=models.CharField(choices=[('REPASSE_REALIZADO', 'Repasses realizados'), ('CARGA_PERIODO_INICIAL', 'Carga período inicial'), ('REPASSE_PREVISTO', 'Repasses previstos'), ('CARGA_ASSOCIACOES', 'Carga de Associações'), ('CARGA_USUARIOS', 'Carga de usuários'), ('CARGA_CENSO', 'Carga de censo'), ('CARGA_REPASSE_PREVISTO_SME', 'Repasses previstos sme'), ('CARGA_DEVOLUCAO_TESOURO', 'Devoluções ao Tesouro')], default='CARGA_ASSOCIACOES', max_length=35, unique=True, verbose_name='tipo de carga'),
        ),
    ]