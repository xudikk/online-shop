# Generated by Django 5.2.1 on 2025-06-13 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_product_price_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
