# Generated by Django 5.1.6 on 2025-02-19 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0004_alter_dailyactivity_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyactivity',
            name='date',
            field=models.DateField(),
        ),
    ]
