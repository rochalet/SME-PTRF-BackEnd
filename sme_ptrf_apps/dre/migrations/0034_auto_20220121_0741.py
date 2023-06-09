# Generated by Django 2.2.10 on 2022-01-21 07:41

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0242_auto_20220120_1148'),
        ('dre', '0033_analiseregularidadeassociacao_motivo_nao_regularidade'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtaParecerTecnico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('arquivo_pdf', models.FileField(blank=True, null=True, upload_to='', verbose_name='Relatório em PDF')),
                ('status_geracao_pdf', models.CharField(choices=[('NAO_GERADO', 'Não gerado'), ('EM_PROCESSAMENTO', 'Em processamento'), ('CONCLUIDO', 'Geração concluída')], default='NAO_GERADO', max_length=20, verbose_name='status Pdf')),
                ('numero_ata', models.IntegerField(blank=True, null=True, verbose_name='Numero da ata')),
                ('data_reuniao', models.DateField(blank=True, null=True, verbose_name='data da reunião')),
                ('hora_reuniao', models.TimeField(default='00:00', verbose_name='Hora da reunião')),
                ('local_reuniao', models.CharField(blank=True, default='', max_length=200, verbose_name='local da reunião')),
                ('comentarios', models.TextField(blank=True, default='', verbose_name='Manifestações, comentários e justificativas')),
                ('preenchida_em', models.DateTimeField(blank=True, null=True, verbose_name='Preenchida em')),
                ('dre', models.ForeignKey(blank=True, limit_choices_to={'tipo_unidade': 'DRE'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='atas_parecer_tecnico_da_dre', to='core.Unidade')),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='atas_parecer_tecnico_dre_do_periodo', to='core.Periodo')),
            ],
            options={
                'verbose_name': 'Ata de Parecer Tecnico',
                'verbose_name_plural': 'Atas de Parecer Tecnicos',
            },
        ),
        migrations.AddField(
            model_name='membrocomissao',
            name='cargo',
            field=models.CharField(blank=True, default='', max_length=65, null=True, verbose_name='Cargo'),
        ),
        migrations.CreateModel(
            name='PresenteAtaDre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('rf', models.CharField(max_length=10, verbose_name='RF')),
                ('nome', models.CharField(blank=True, default='', max_length=200, verbose_name='Nome')),
                ('cargo', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Cargo')),
                ('ata', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='presentes_na_ata', to='dre.AtaParecerTecnico')),
            ],
            options={
                'verbose_name': 'Presente da ata DRE',
                'verbose_name_plural': 'Presentes das atas DRE',
            },
        ),
        migrations.CreateModel(
            name='ParametrosDre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('comissao_exame_contas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comissao_com_exame_contas', to='dre.Comissao')),
            ],
            options={
                'verbose_name': 'Parâmetro DRE',
                'verbose_name_plural': 'Parâmetros DRE',
            },
        ),
    ]
