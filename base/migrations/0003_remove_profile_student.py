# Generated by Django 4.2.13 on 2024-07-12 01:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_student_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='student',
        ),
    ]