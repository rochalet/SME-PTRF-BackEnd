# Generated by Django 2.2.10 on 2021-05-27 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0170_auto_20210510_1420'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='funcdredadosdadiretoria',
            options={'default_permissions': (), 'managed': False, 'permissions': (('access_dados_diretoria', '[DRE] Pode acessar Dados da Diretoria.'), ('change_dados_diretoria', '[DRE] Pode atualizar Dados da Diretoria.')), 'verbose_name': '[DRE] Dados da diretoria', 'verbose_name_plural': '[DRE] Dados da diretoria'},
        ),
    ]
