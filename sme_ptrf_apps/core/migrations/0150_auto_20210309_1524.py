# Generated by Django 2.2.10 on 2021-03-09 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0149_auto_20210309_1523'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ambiente',
            unique_together=set(),
        ),
    ]