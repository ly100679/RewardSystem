# Generated by Django 2.2.2 on 2019-07-05 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_competition_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='expert',
            name='field',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]