# Generated by Django 2.2.1 on 2019-05-15 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20190516_0112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='overview',
            field=models.TextField(),
        ),
    ]