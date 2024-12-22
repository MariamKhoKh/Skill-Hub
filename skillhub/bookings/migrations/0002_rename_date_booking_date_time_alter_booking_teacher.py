# Generated by Django 5.1.4 on 2024-12-22 14:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
        ('teaching', '0003_remove_teacherprofile_skills_teacherprofile_skills'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='date',
            new_name='date_time',
        ),
        migrations.AlterField(
            model_name='booking',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='teaching.teacherprofile'),
        ),
    ]
