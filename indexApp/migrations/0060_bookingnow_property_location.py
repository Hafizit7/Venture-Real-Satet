# Generated by Django 4.1.2 on 2022-11-07 04:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indexApp', '0059_remove_propertypost_video_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingnow',
            name='property_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='indexApp.location'),
        ),
    ]
