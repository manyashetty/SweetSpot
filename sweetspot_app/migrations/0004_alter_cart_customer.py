# Generated by Django 5.1.2 on 2024-10-15 11:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sweetspot_app', '0003_alter_customer_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sweetspot_app.customer'),
        ),
    ]
