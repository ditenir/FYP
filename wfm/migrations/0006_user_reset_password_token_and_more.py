# Generated by Django 4.1.7 on 2023-05-14 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wfm', '0005_calculation_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reset_password_token',
            field=models.CharField(max_length=63, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='reset_password_token_valid_until',
            field=models.DateTimeField(null=True),
        ),
    ]
