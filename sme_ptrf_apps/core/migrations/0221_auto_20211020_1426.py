# Generated by Django 2.2.10 on 2021-10-20 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0220_auto_20211018_0741'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacao',
            name='prestacao_conta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notificacoes_da_prestacao', to='core.PrestacaoConta'),
        ),
        migrations.AddField(
            model_name='notificacao',
            name='unidade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notificacoes_da_unidade', to='core.Unidade'),
        ),
        migrations.AlterField(
            model_name='notificacao',
            name='categoria',
            field=models.CharField(choices=[('COMENTARIO_PC', 'Comentário na prestação de contas'), ('ELABORACAO_PC', 'Elaboração de PC'), ('ANALISE_PC', 'Análise de PC'), ('DEVOLUCAO_PC', 'Devolução de PC para ajustes')], default='COMENTARIO_PC', max_length=15, verbose_name='Categoria'),
        ),
    ]