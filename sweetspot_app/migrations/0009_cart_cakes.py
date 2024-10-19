# Generated by Django 5.1.2 on 2024-10-17 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sweetspot_app', '0008_remove_cart_cakes'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='cakes',
            field=models.ManyToManyField(related_name='carts', through='sweetspot_app.CartCake', to='sweetspot_app.cake'),
        ),
    ]
