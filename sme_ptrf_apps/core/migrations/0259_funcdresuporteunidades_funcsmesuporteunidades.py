# Generated by Django 2.2.10 on 2022-06-09 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0258_auto_20220607_1340'),
    ]

    operations = [
        migrations.CreateModel(
            name='FuncDreSuporteUnidades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '[DRE] Suporte às unidades',
                'verbose_name_plural': '[DRE] Suporte às unidades',
                'permissions': (('access_suporte_unidades_dre', '[DRE] Pode acessar o suporte às unidades (DRE).'),),
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='FuncSmeSuporteUnidades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '[SME] Suporte às unidades',
                'verbose_name_plural': '[SME] Suporte às unidades',
                'permissions': (('access_suporte_unidades_sme', '[SME] Pode acessar o suporte às unidades (SME).'),),
                'managed': False,
                'default_permissions': (),
            },
        ),
    ]