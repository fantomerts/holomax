# Generated by Django 3.2.7 on 2022-01-06 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0017_auto_20220106_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='nbonuscard',
            name='number',
            field=models.IntegerField(blank=True, help_text='Enter a number of card', null=True),
        ),
    ]
