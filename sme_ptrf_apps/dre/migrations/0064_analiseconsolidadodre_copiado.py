# Generated by Django 2.2.10 on 2022-11-28 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dre', '0063_auto_20221111_1042'),
    ]

    operations = [
        migrations.AddField(
            model_name='analiseconsolidadodre',
            name='copiado',
            field=models.BooleanField(default=False, verbose_name='é uma copiá?'),
        ),
    ]