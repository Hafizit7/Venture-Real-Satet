# Generated by Django 4.1.2 on 2022-10-29 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indexApp', '0040_alter_agent_options_remove_why_chosse_us_title_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Property_Post',
            new_name='PropertyPost',
        ),
    ]