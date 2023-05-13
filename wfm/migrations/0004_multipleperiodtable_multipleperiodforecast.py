# Generated by Django 4.1.7 on 2023-05-11 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wfm', '0003_punctualreverseforecast'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultiplePeriodTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zone', models.CharField(max_length=63, null=True)),
                ('language', models.CharField(max_length=15, null=True)),
                ('media_type', models.CharField(max_length=15, null=True)),
                ('agents_table', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='MultiplePeriodForecast',
            fields=[
                ('calculation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wfm.calculation')),
                ('total_agents_number', models.IntegerField()),
                ('agents_per_criteria', models.ManyToManyField(to='wfm.multipleperiodtable')),
            ],
            bases=('wfm.calculation',),
        ),
    ]