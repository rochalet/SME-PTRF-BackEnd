# Generated by Django 2.2.10 on 2020-07-23 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0056_associacao_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='membroassociacao',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email'),
        ),
    ]