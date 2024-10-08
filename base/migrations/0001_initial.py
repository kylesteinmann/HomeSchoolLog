# Generated by Django 4.2.13 on 2024-07-18 01:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StateRequirements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=50, null=True)),
                ('core_hours', models.DecimalField(decimal_places=0, max_digits=10)),
                ('total_hours', models.DecimalField(decimal_places=0, max_digits=10)),
                ('year_start', models.DateField()),
                ('year_end', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('birthdate', models.DateField()),
                ('grade', models.CharField(choices=[('Kindergarten', 'Kindergarten'), ('First', 'First'), ('Second', 'Second'), ('Third', 'Third'), ('Fourth', 'Fourth'), ('Fifth', 'Fifth'), ('Sixth', 'Sixth'), ('Seventh', 'Seventh'), ('Eigth', 'Eigth'), ('Ninth', 'Ninth'), ('Tenth', 'Tenth'), ('Eleventh', 'Eleventh'), ('Twelfth', 'Twelfth')], max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to='base.staterequirements')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
