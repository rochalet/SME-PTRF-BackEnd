# Generated by Django 2.2.10 on 2021-02-12 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('despesas', '0032_rateiodespesa_update_conferido'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tipocusteio',
            unique_together={('nome',)},
        ),
    ]
