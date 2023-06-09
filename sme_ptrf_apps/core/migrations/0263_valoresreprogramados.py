# Generated by Django 2.2.10 on 2022-07-07 09:52

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0262_merge_20220623_1056'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValoresReprogramados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('aplicacao_recurso', models.CharField(choices=[('CAPITAL', 'Capital'), ('CUSTEIO', 'Custeio'), ('LIVRE', 'Livre Aplicação')], max_length=15, verbose_name='Tipo de aplicação do recurso')),
                ('valor_ue', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Valor UE')),
                ('valor_dre', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Valor DRE')),
                ('acao_associacao', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='valores_reprogramados_da_acao', to='core.AcaoAssociacao')),
                ('associacao', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='valores_reprogramados_associacao', to='core.Associacao')),
                ('conta_associacao', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='valores_reprogramados_da_conta', to='core.ContaAssociacao')),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='valores_reprogramados', to='core.Periodo')),
            ],
            options={
                'verbose_name': 'Valores reprogramados',
                'verbose_name_plural': '18.0) Valores reprogramados',
                'unique_together': {('associacao', 'periodo', 'aplicacao_recurso')},
            },
        ),
    ]
