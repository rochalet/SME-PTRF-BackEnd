# Generated by Django 2.2.10 on 2022-01-14 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0240_auto_20220103_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='ata',
            name='previa',
            field=models.BooleanField(default=False, verbose_name='É prévia?'),
        ),
        migrations.AlterField(
            model_name='ata',
            name='prestacao_conta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='atas_da_prestacao', to='core.PrestacaoConta'),
        ),
    ]
