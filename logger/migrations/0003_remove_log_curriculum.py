# Generated by Django 4.2.13 on 2024-07-18 00:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0002_rename_logs_log'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='curriculum',
        ),
    ]
