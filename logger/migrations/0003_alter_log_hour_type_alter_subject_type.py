# Generated by Django 4.2.13 on 2024-07-18 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0002_rename_discription_log_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='hour_type',
            field=models.CharField(choices=[('Core', 'Core'), ('Elective', 'Elective')], max_length=255),
        ),
        migrations.AlterField(
            model_name='subject',
            name='type',
            field=models.CharField(choices=[('Core Away From Home', 'Core Away From Home'), ('Core At Home', 'Core At Home'), ('Elective', 'Elective')], max_length=255),
        ),
    ]
