# Generated by Django 2.2.1 on 2019-05-20 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
