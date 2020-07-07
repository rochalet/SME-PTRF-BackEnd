# Generated by Django 2.2.10 on 2020-06-02 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20200602_1734'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ata',
            name='parecer_concelho',
        ),
        migrations.AddField(
            model_name='ata',
            name='parecer_conselho',
            field=models.CharField(choices=[('APROVADA', 'Aprovada'), ('REJEITADA', 'Rejeitada'), ('RESSALVAS', 'Aprovada com ressalvas')], default='APROVADA', max_length=20, verbose_name='parecer do conselho'),
        ),
    ]