# Generated by Django 4.0.10 on 2023-03-18 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0004_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.JSONField(default=dict),
        ),
    ]