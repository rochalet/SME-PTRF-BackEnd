# Generated by Django 2.2.10 on 2021-04-26 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_atualiza_e_servidor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='tipo_usuario',
        ),
    ]