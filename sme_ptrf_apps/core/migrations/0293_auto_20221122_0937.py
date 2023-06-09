# Generated by Django 2.2.10 on 2022-11-22 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('despesas', '0052_auto_20220906_1331'),
        ('receitas', '0047_auto_20220905_0950'),
        ('core', '0292_auto_20221110_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitacaoacertodocumento',
            name='despesa_incluida',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solicitacao_acerto_de_documento_que_incluiu_a_despesa', to='despesas.Despesa'),
        ),
        migrations.AddField(
            model_name='solicitacaoacertodocumento',
            name='esclarecimentos',
            field=models.TextField(blank=True, default=None, max_length=300, null=True, verbose_name='Esclarecimentos'),
        ),
        migrations.AddField(
            model_name='solicitacaoacertodocumento',
            name='justificativa',
            field=models.TextField(blank=True, default=None, max_length=300, null=True, verbose_name='Justificativa'),
        ),
        migrations.AddField(
            model_name='solicitacaoacertodocumento',
            name='receita_incluida',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solicitacao_acerto_de_documento_que_incluiu_a_receita', to='receitas.Receita'),
        ),
        migrations.AddField(
            model_name='solicitacaoacertodocumento',
            name='status_realizacao',
            field=models.CharField(choices=[('PENDENTE', 'Pendente'), ('REALIZADO', 'Realizado'), ('JUSTIFICADO', 'Justificado')], default='PENDENTE', max_length=15, verbose_name='Status de realização'),
        ),
    ]
