# Generated by Django 4.1.2 on 2022-11-03 09:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexApp', '0052_faq'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingNow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator('^(\\+?\\d{0,4})?\\s?-?\\s?(\\(?\\d{3}\\)?)\\s?-?\\s?(\\(?\\d{3}\\)?)\\s?-?\\s?(\\(?\\d{4}\\)?)?$', 'The phone number provided is invalid')])),
                ('job_designation', models.CharField(max_length=50)),
                ('property_type', models.CharField(max_length=50, null=True)),
                ('property_size', models.IntegerField()),
                ('roperty_description', models.TextField()),
            ],
            options={
                'verbose_name': 'BookingNow',
                'verbose_name_plural': 'Booking Now',
            },
        ),
    ]