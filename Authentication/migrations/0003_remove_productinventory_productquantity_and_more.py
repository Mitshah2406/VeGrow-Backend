# Generated by Django 4.0.10 on 2023-03-21 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0002_allproductlist_productmarketprice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productinventory',
            name='productQuantity',
        ),
        migrations.AddField(
            model_name='productinventory',
            name='initialBidPrice',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productinventory',
            name='unit',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='productinventory',
            name='unitValue',
            field=models.CharField(max_length=254, null=True),
        ),
    ]
