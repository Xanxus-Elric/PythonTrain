# Generated by Django 2.2.4 on 2019-08-28 07:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Issue', '0004_auto_20190828_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='Publish',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
