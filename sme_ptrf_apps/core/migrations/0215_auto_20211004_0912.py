# Generated by Django 2.2.10 on 2021-10-04 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0214_auto_20210930_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestacaoconta',
            name='status',
            field=models.CharField(choices=[('NAO_APRESENTADA', 'Não apresentada'), ('NAO_RECEBIDA', 'Não recebida'), ('RECEBIDA', 'Recebida'), ('EM_ANALISE', 'Em análise'), ('DEVOLVIDA', 'Devolvida para acertos'), ('DEVOLVIDA_RETORNADA', 'Retornada após acertos'), ('DEVOLVIDA_RECEBIDA', 'Recebida após acertos'), ('APROVADA', 'Aprovada'), ('APROVADA_RESSALVA', 'Aprovada com ressalvas'), ('REPROVADA', 'Reprovada'), ('EM_PROCESSAMENTO', 'Em processamento')], default='NAO_APRESENTADA', max_length=20, verbose_name='status'),
        ),
    ]
