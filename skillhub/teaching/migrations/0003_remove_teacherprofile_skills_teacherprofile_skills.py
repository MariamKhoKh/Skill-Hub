# Generated by Django 5.1.4 on 2024-12-21 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teaching', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacherprofile',
            name='skills',
        ),
        migrations.AddField(
            model_name='teacherprofile',
            name='skills',
            field=models.ManyToManyField(blank=True, to='teaching.skill'),
        ),
    ]
