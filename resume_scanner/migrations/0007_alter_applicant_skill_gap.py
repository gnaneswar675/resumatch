# Generated by Django 5.1.7 on 2025-04-10 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume_scanner', '0006_remove_applicant_recommended_jobs_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='skill_gap',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
