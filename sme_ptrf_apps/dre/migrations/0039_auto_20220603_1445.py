# Generated by Django 2.2.10 on 2022-06-03 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0257_auto_20220518_1659'),
        ('dre', '0038_consolidadodre'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='consolidadodre',
            unique_together={('periodo', 'dre')},
        ),
    ]
