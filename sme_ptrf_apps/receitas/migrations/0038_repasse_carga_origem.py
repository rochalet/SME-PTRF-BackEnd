# Generated by Django 2.2.10 on 2021-10-07 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0216_prestacaoconta_data_recebimento_apos_acertos'),
        ('receitas', '0037_tiporeceita_possui_detalhamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='repasse',
            name='carga_origem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='repasses_criados', to='core.Arquivo'),
        ),
    ]
