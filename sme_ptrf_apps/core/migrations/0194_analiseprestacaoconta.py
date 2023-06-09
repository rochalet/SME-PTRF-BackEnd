# Generated by Django 2.2.10 on 2021-08-17 15:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0193_funcdrefornecedores_funcsmefornecedores'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalisePrestacaoConta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('status', models.CharField(choices=[('EM_ANALISE', 'Em análise'), ('DEVOLVIDA', 'Devolvida para acertos'), ('APROVADA', 'Aprovada'), ('APROVADA_RESSALVA', 'Aprovada com ressalvas'), ('REPROVADA', 'Reprovada')], default='EM_ANALISE', max_length=20, verbose_name='status')),
                ('devolucao_prestacao_conta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='analises_da_devolucao', to='core.DevolucaoPrestacaoConta')),
                ('prestacao_conta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analises_da_prestacao', to='core.PrestacaoConta')),
            ],
            options={
                'verbose_name': 'Análise de prestação de contas',
                'verbose_name_plural': '15.0) Análises de prestações de contas',
            },
        ),
    ]
