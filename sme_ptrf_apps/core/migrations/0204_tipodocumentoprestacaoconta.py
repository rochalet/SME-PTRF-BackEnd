# Generated by Django 2.2.10 on 2021-09-09 13:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0203_auto_20210901_1408'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoDocumentoPrestacaoConta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=160, verbose_name='Nome')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
            options={
                'verbose_name': 'Documento de prestação de contas',
                'verbose_name_plural': '16.4) Documentos de prestação de contas',
            },
        ),
    ]
