# Generated by Django 5.1.7 on 2025-03-31 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('skills', models.TextField()),
                ('experience', models.IntegerField()),
                ('resume_file', models.FileField(upload_to='resumes/')),
            ],
        ),
    ]
