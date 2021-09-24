# Generated by Django 2.2.10 on 2021-08-26 13:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0200_merge_20210823_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoAcertoLancamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=160, verbose_name='Nome')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('categoria', models.CharField(choices=[('BASICO', 'Básico'), ('DEVOLUCAO', 'Devolução')], default='BASICO', max_length=35, verbose_name='status')),
            ],
            options={
                'verbose_name': 'Tipo de acerto em lançamentos',
                'verbose_name_plural': '15.1) Tipos de acerto em lançamentos',
            },
        ),
    ]