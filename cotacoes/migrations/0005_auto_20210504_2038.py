# Generated by Django 3.2 on 2021-05-04 23:38

import cotacoes.enums
from decimal import Decimal
from django.db import migrations, models
import django.utils.timezone
import django_enum_choices.choice_builders
import django_enum_choices.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cotacoes', '0004_auto_20210503_0121'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ConfiguracaoApp',
        ),
        migrations.AddField(
            model_name='monitoramento',
            name='ultima_atualizacao',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data/Hora da última atualização do valor da ação'),
        ),
        migrations.AddField(
            model_name='monitoramento',
            name='variacao',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=4, verbose_name='Variação do valor da ação'),
        ),
        migrations.AlterField(
            model_name='configuracaotitulo',
            name='intervalo',
            field=django_enum_choices.fields.EnumChoiceField(choice_builder=django_enum_choices.choice_builders.value_value, choices=[('1 min', '1 min'), ('15 min', '15 min'), ('30 mins', '30 mins'), ('45 mins', '45 mins'), ('1 hora', '1 hora')], default=cotacoes.enums.Intervalo['quinze_minutos'], enum_class=cotacoes.enums.Intervalo, max_length=7),
        ),
        migrations.AlterField(
            model_name='monitoramento',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Timestamp da coleta'),
        ),
    ]