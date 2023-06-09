# Generated by Django 2.2.10 on 2021-11-05 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0226_auto_20211103_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacao',
            name='prestacao_conta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notificacoes_da_prestacao', to='core.PrestacaoConta'),
        ),
        migrations.AlterField(
            model_name='notificacao',
            name='unidade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notificacoes_da_unidade', to='core.Unidade'),
        ),
    ]
