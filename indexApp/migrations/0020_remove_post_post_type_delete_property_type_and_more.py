# Generated by Django 4.1.2 on 2022-10-27 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexApp', '0019_property_type_alter_post_post_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_type',
        ),
        migrations.DeleteModel(
            name='Property_type',
        ),
        migrations.AddField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('feature', 'feature'), ('apartment', 'apartment'), ('land', 'land'), ('recent', 'recent')], max_length=100, null=True),
        ),
    ]
