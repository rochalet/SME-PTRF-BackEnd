# Generated by Django 2.2.10 on 2021-06-17 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0184_merge_20210617_1004'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='funcuerecebimentodenotificacoes',
            options={'default_permissions': (), 'managed': False, 'permissions': (('recebe_notificacao_inicio_periodo_prestacao_de_contas', '[UE] Pode receber Notificação Início Período Prestação De Contas.'), ('recebe_notificacao_pendencia_envio_prestacao_de_contas', '[UE] Pode receber Notificação pendência envio Prestação De Contas.'), ('recebe_notificacao_proximidade_inicio_prestacao_de_contas', '[UE] Pode receber Notificação Proximidade Início Prestação De Contas.'), ('recebe_notificacao_prestacao_de_contas_devolvida_para_acertos', '[UE] Pode receber Notificação Prestação de Contas Devolvida para Acertos')), 'verbose_name': '[UE] Recebimento de notificações', 'verbose_name_plural': '[UE] Recebimento de notificações'},
        ),
    ]
