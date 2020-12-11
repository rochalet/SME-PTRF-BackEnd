# Generated by Django 2.2.10 on 2020-11-24 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0115_devolucaoaotesouro_visao_criacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='cobrancaprestacaoconta',
            name='associacao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cobrancas_prestacoes_de_conta_da_associacao', to='core.Associacao'),
        ),
        migrations.AddField(
            model_name='cobrancaprestacaoconta',
            name='periodo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cobrancas_prestacoes_de_conta_no_periodo', to='core.Periodo'),
        ),
        migrations.AlterField(
            model_name='cobrancaprestacaoconta',
            name='prestacao_conta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cobrancas_da_prestacao', to='core.PrestacaoConta'),
        ),
    ]