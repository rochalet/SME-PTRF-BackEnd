# Generated by Django 2.2.10 on 2021-11-03 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0225_auto_20211103_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='associacao',
            name='cargo_substituto_presidente_ausente',
            field=models.CharField(blank=True, choices=[('PRESIDENTE_DIRETORIA_EXECUTIVA', 'Presidente da diretoria executiva'), ('VICE_PRESIDENTE_DIRETORIA_EXECUTIVA', 'Vice-Presidente da diretoria executiva'), ('SECRETARIO', 'Secretario'), ('TESOUREIRO', 'Tesoureiro'), ('VOGAL_1', 'Vogal 1'), ('VOGAL_2', 'Vogal 2'), ('VOGAL_3', 'Vogal 3'), ('VOGAL_4', 'Vogal 4'), ('VOGAL_5', 'Vogal 5')], default=None, max_length=65, null=True, verbose_name='Cargo substituto do presidente ausente'),
        ),
    ]