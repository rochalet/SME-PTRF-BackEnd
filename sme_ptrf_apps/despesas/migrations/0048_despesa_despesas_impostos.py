# Generated by Django 2.2.10 on 2022-04-04 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('despesas', '0047_auto_20220325_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='despesa',
            name='despesas_impostos',
            field=models.ManyToManyField(blank=True, related_name='despesa_geradora', to='despesas.Despesa'),
        ),
    ]
