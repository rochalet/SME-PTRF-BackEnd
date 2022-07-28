# Generated by Django 2.2.10 on 2022-07-25 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0267_auto_20220722_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipoacertolancamento',
            name='categoria',
            field=models.CharField(choices=[('DEVOLUCAO', 'Devolução ao tesouro'), ('EDICAO_LANCAMENTO', 'Edição do lançamento'), ('EXCLUSAO_LANCAMENTO', 'Exclusão do lançamento'), ('AJUSTES_EXTERNOS', 'Ajustes externos'), ('SOLICITACAO_ESCLARECIMENTO', 'Solicitação de esclarecimento')], max_length=35, verbose_name='Categoria'),
        ),
    ]
