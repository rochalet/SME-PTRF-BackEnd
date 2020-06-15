# Generated by Django 2.2.10 on 2020-06-05 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_remove_associacao_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='demonstrativofinanceiro',
            name='arquivo',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='demonstrativofinanceiro',
            name='conta_associacao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='demonstrativos_financeiros', to='core.ContaAssociacao'),
        ),
        migrations.AddField(
            model_name='demonstrativofinanceiro',
            name='prestacao_conta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='demonstrativos_da_prestacao', to='core.PrestacaoConta'),
        ),
        migrations.AlterField(
            model_name='demonstrativofinanceiro',
            name='acao_associacao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='demonstrativos_financeiros', to='core.AcaoAssociacao'),
        ),
    ]
