# Generated by Django 2.2.10 on 2021-02-04 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0140_auto_20210203_1423'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together={('nome',)},
        ),
    ]
