# Generated by Django 2.2.10 on 2022-03-07 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('despesas', '0040_auto_20220305_0831'),
    ]

    operations = [
        migrations.AddField(
            model_name='despesa',
            name='retem_imposto',
            field=models.BooleanField(default=False, verbose_name='Retém imposto?'),
        ),
    ]
