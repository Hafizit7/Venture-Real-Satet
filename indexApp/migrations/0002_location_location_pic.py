# Generated by Django 4.1.2 on 2022-10-15 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='location_pic',
            field=models.ImageField(null=True, upload_to='location_img/'),
        ),
    ]
