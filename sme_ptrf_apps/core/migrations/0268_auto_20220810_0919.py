# Generated by Django 2.2.10 on 2022-08-10 09:19

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0267_auto_20220808_0918'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametros',
            name='texto_pagina_valores_reprogramados_dre',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='Texto da página de valores reprogramados (DRE)'),
        ),
        migrations.AddField(
            model_name='parametros',
            name='texto_pagina_valores_reprogramados_ue',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='Texto da página de valores reprogramados (UE)'),
        ),
    ]
