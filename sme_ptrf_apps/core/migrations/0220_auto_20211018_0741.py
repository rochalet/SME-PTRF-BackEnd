# Generated by Django 2.2.10 on 2021-10-18 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0219_merge_20211013_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analiseprestacaoconta',
            name='status_versao',
            field=models.CharField(choices=[('NAO_GERADO', 'Não gerado'), ('EM_PROCESSAMENTO', 'Em processamento'), ('CONCLUIDO', 'Geração concluída')], default='NAO_GERADO', max_length=20, verbose_name='Status da geração do documento'),
        ),
        migrations.AlterField(
            model_name='analiseprestacaoconta',
            name='versao',
            field=models.CharField(choices=[('-', '-'), ('FINAL', 'final'), ('RASCUNHO', 'rascunho')], default='-', max_length=20, verbose_name='Versão do documento'),
        ),
    ]