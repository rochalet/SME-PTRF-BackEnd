# Generated by Django 2.2.10 on 2020-07-29 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('despesas', '0026_rateiodespesa_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipodocumento',
            name='numero_documento_digitado',
            field=models.BooleanField(default=False, verbose_name='Solicitar a digitação do número do documento?'),
        ),
    ]