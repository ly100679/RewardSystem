# Generated by Django 2.2.2 on 2019-07-06 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20190705_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='display',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='research',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
