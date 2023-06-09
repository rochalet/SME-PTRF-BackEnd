# Generated by Django 2.2.10 on 2021-05-28 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0171_auto_20210527_1428'),
    ]

    operations = [
        migrations.CreateModel(
            name='FuncDreAtribuicaoPorUe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '[DRE] Atribuição por UE',
                'verbose_name_plural': '[DRE] Atribuições por UE',
                'permissions': (('access_atribuicao_por_ue', '[DRE] Pode acessar Atribuição por UE.'), ('change_atribuicao_por_ue', '[DRE] Pode atualizar Atribuição por UE.')),
                'managed': False,
                'default_permissions': (),
            },
        ),
    ]
