# Generated by Django 3.2.12 on 2023-06-26 10:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Repair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repairTitle', models.CharField(max_length=100, verbose_name='Issue Title')),
                ('repairDescription', models.TextField(verbose_name='Issue Description')),
                ('repairStatus', models.CharField(default='Processing', max_length=20, verbose_name='Issue Status (Leave as Default)')),
                ('dateLogged', models.DateField(default=django.utils.timezone.now)),
                ('repairImage', models.ImageField(blank=True, upload_to='repair_images', verbose_name='Issue Evidence')),
                ('suNumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Student Number')),
            ],
        ),
    ]
