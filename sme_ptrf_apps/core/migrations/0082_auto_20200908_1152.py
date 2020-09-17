# Generated by Django 2.2.10 on 2020-09-08 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0081_auto_20200902_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestacaoconta',
            name='status',
            field=models.CharField(choices=[('DOCS_PENDENTES', 'Documentos pendentes'), ('NAO_RECEBIDA', 'Não recebida'), ('RECEBIDA', 'Recebida'), ('EM_ANALISE', 'Em análise'), ('DEVOLVIDA', 'Devolvida para acertos'), ('APROVADA', 'Aprovada'), ('REPROVADA', 'Reprovada')], default='DOCS_PENDENTES', max_length=15, verbose_name='status'),
        ),
    ]
