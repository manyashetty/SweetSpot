# Generated by Django 5.1.2 on 2024-10-14 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sweetspot_app', '0002_customer_address_customer_city_customer_phone_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.TextField(default='No address provided'),
        ),
    ]
