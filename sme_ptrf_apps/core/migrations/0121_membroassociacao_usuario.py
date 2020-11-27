# Generated by Django 2.2.10 on 2020-11-26 16:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0120_auto_20201125_1905'),
    ]

    operations = [
        migrations.AddField(
            model_name='membroassociacao',
            name='usuario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='membro', to=settings.AUTH_USER_MODEL),
        ),
    ]
