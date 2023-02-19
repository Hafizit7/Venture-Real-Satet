# Generated by Django 4.1.2 on 2022-10-29 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexApp', '0034_property_post_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property_post',
            name='post_pic',
            field=models.ImageField(blank=True, null=True, upload_to='features_post_img/'),
        ),
        migrations.AlterField(
            model_name='property_post',
            name='post_title',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='property_post',
            name='post_type',
            field=models.ManyToManyField(blank=True, related_name='pro_type', to='indexApp.property_type'),
        ),
    ]