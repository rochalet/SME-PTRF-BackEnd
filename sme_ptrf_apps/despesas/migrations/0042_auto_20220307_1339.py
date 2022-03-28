# Generated by Django 2.2.10 on 2022-03-07 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('despesas', '0041_despesa_retem_imposto'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipodocumento',
            name='eh_documento_de_retencao_de_imposto',
            field=models.BooleanField(default=False, verbose_name='É documento de retenção de imposto?'),
        ),
        migrations.AddField(
            model_name='tipodocumento',
            name='pode_reter_imposto',
            field=models.BooleanField(default=False, verbose_name='Pode reter imposto?'),
        ),
    ]