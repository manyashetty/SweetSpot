# Generated by Django 5.1.2 on 2024-10-15 11:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sweetspot_app', '0004_alter_cart_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sweetspot_app.customer'),
        ),
    ]
