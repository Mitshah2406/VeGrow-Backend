# Generated by Django 4.0.10 on 2023-03-21 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='allproductlist',
            name='productMarketPrice',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]
