# Generated by Django 2.2.10 on 2021-06-14 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0176_auto_20210614_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacao',
            name='remetente',
            field=models.CharField(choices=[('SISTEMA', 'Sistema'), ('DRE', 'DRE'), ('SME', 'SME')], default='SISTEMA', max_length=15, verbose_name='Remetente'),
        ),
    ]
