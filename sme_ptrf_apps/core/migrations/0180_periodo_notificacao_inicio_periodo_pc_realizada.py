# Generated by Django 2.2.10 on 2021-06-15 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0179_funcuerecebimentodenotificacoes'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodo',
            name='notificacao_inicio_periodo_pc_realizada',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Notificação início período de PC realizada'),
        ),
    ]