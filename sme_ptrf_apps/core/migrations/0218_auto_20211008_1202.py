# Generated by Django 2.2.10 on 2021-10-08 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0217_analiseprestacaoconta_arquivo_pdf_criado_em'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analiseprestacaoconta',
            name='status_versao',
            field=models.CharField(choices=[('NAO_GERADO', 'Não gerado'), ('EM_PROCESSAMENTO', 'Em processamento'), ('CONCLUIDO', 'Geração concluída')], default='NAO_GERADO', max_length=20, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='analiseprestacaoconta',
            name='versao',
            field=models.CharField(choices=[('-', '-'), ('FINAL', 'final'), ('RASCUNHO', 'rascunho')], default='-', max_length=20, verbose_name='versão'),
        ),
    ]
