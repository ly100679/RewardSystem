# Generated by Django 2.2.2 on 2019-07-04 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_expertlist_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='expertlist',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='project',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Student'),
        ),
        migrations.AlterField(
            model_name='project',
            name='competition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Competition'),
        ),
    ]
