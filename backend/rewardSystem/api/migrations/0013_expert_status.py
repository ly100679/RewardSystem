# Generated by Django 2.2.2 on 2019-07-06 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_remove_expertlist_competition'),
    ]

    operations = [
        migrations.AddField(
            model_name='expert',
            name='status',
            field=models.CharField(default='0', max_length=100),
        ),
    ]
