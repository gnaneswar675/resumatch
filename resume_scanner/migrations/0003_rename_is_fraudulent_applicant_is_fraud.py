# Generated by Django 5.1.7 on 2025-04-09 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resume_scanner', '0002_applicant_job_delete_resume_applicant_job'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applicant',
            old_name='is_fraudulent',
            new_name='is_fraud',
        ),
    ]
