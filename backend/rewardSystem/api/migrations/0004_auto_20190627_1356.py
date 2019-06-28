# Generated by Django 2.2.2 on 2019-06-27 05:56

import api.enum
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190627_1144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expert',
            old_name='expert_name',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='opinion',
            name='opinion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='opinion',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_type',
            field=models.CharField(blank=True, choices=[(api.enum.ProjectType('Project'), 'Project'), (api.enum.ProjectType('Paper'), 'Paper')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School'),
        ),
        migrations.AlterField(
            model_name='project',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='project_video/'),
        ),
        migrations.AlterField(
            model_name='student',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='tel',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
