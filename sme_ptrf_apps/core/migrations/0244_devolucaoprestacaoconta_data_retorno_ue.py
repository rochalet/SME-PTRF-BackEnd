# Generated by Django 2.2.10 on 2022-02-04 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0243_merge_20220121_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='devolucaoprestacaoconta',
            name='data_retorno_ue',
            field=models.DateField(blank=True, null=True, verbose_name='data do retorno pela ue'),
        ),
    ]