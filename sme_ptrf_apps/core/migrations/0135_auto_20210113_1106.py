# Generated by Django 2.2.10 on 2021-01-13 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dre', '0021_motivoaprovacaoressalva'),
        ('core', '0134_remove_membroassociacao_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prestacaoconta',
            name='motivo_aprovacao_ressalva',
        ),
        migrations.AddField(
            model_name='prestacaoconta',
            name='motivos_aprovacao_ressalva',
            field=models.ManyToManyField(blank=True, null=True, to='dre.MotivoAprovacaoRessalva'),
        ),
        migrations.AddField(
            model_name='prestacaoconta',
            name='outros_motivos_aprovacao_ressalva',
            field=models.TextField(blank=True, default='', verbose_name='Outros motivos para aprovação com ressalvas pela DRE'),
        ),
    ]
