# Generated by Django 2.2.8 on 2020-01-14 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0002_auto_20200113_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='total_time',
            field=models.FloatField(default=0),
        ),
    ]
