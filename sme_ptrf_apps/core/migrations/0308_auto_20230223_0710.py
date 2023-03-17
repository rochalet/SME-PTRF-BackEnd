# Generated by Django 2.2.10 on 2023-02-23 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0307_auto_20230215_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipoacertolancamento',
            name='categoria',
            field=models.CharField(choices=[('DEVOLUCAO', 'Devolução ao tesouro'), ('EDICAO_LANCAMENTO', 'Edição do lançamento'), ('CONCILIACAO_LANCAMENTO', 'Conciliação do lançamento'), ('DESCONCILIACAO_LANCAMENTO', 'Desconciliação do lançamento'), ('EXCLUSAO_LANCAMENTO', 'Exclusão do lançamento'), ('AJUSTES_EXTERNOS', 'Ajustes externos'), ('SOLICITACAO_ESCLARECIMENTO', 'Solicitação de esclarecimento')], max_length=35, verbose_name='Categoria'),
        ),
    ]